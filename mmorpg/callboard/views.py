from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from mmorpg.tasks.User_greeting import send_response_email, send_response_for_author_email

from .forms import AdvertisementFormEdit, CreateAdvertisementForm, MediaContentForm, UserResponseForm
from .models import Advertisement, MediaContent, UserBoard, UserResponse

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
class PostList(ListView):
    model = Advertisement
    template_name = 'post_list.html'
    context_object_name = 'postlist'
    ordering = ['-date_creation']
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        for advertisement in context['postlist']:
            media_content = MediaContent.objects.filter(advertisement=advertisement, media_type='image').first()
            advertisement.media_content = media_content
        
        return context

class CreateAdvertisement(LoginRequiredMixin, CreateView):
    model = Advertisement
    context_object_name = 'advertisement'
    template_name = 'create_advertisement.html'
    form_class = CreateAdvertisementForm
    success_url = reverse_lazy('home')
    def form_valid(self, form):
       
        user_board, created = UserBoard.objects.get_or_create(author=self.request.user)
        form.instance.author = user_board
        response = super().form_valid(form)
        advertisement = self.object 
        self.create_media_content(self.request, advertisement.pk)
        
        return response
    def create_media_content(self, request, advertisement_id):
        advertisement_instance = Advertisement.objects.get(pk=advertisement_id)
        media_file = request.FILES.get('media_file')
        if media_file:
            MediaContent.objects.create(
                advertisement=advertisement_instance,
                media_type='image',
                media_file=media_file
            )

class AdvertisementDetail(LoginRequiredMixin, DetailView):
    model = Advertisement
    template_name = 'detail_post.html'
    context_object_name = 'post'
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        cache_key = f'post_{pk}'
        post = get_object_or_404(Advertisement.objects.filter(pk=pk))
        return post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        media_content = MediaContent.objects.filter(advertisement=context['post'], media_type='image').first()
        context['post'].media_content = media_content
        
        return context
    
class AdvertisementDetailUpdate(LoginRequiredMixin, UpdateView):
    model = Advertisement
    template_name = 'edit_post.html'
    context_object_name = 'edit_post'
    form_class = AdvertisementFormEdit
    success_url = reverse_lazy(viewname='home')
    def form_valid(self, form):
        response = super().form_valid(form)
        advertisement = self.object
        self.update_media_content(self.request, advertisement.pk)
        return response
    def update_media_content(self, request, advertisement_id):
        advertisement_instance = Advertisement.objects.get(pk=advertisement_id)
        media_file = request.FILES.get('media_file')
        if media_file:
            media = MediaContent.objects.get(
                advertisement=advertisement_instance,
            )
            media.media_type = 'image'
            media.media_file = media_file
            media.save()

class AdvertisementDelete(LoginRequiredMixin, DeleteView):
    model = Advertisement
    template_name = 'delete_post.html'
    context_object_name = 'delete_post'
    fields = ('title', 'date_creation')
    success_url = reverse_lazy(viewname='home')

class AdvertisementResponseView(LoginRequiredMixin, DetailView):
    template_name = 'advertisement_detail.html'

    def get(self, request, pk):
        advertisement = Advertisement.objects.get(pk=pk)
        responses = UserResponse.objects.filter(advertisement=advertisement)
        response_form = UserResponseForm()
        
        context = {
            'advertisement': advertisement,
            'responses': responses,
            'response_form': response_form,
        }
        
        return render(request, self.template_name, context)

    def post(self, request, pk):
        advertisement = Advertisement.objects.get(pk=pk)
        responses = UserResponse.objects.filter(advertisement=advertisement)
        response_form = UserResponseForm(request.POST)
        
        if response_form.is_valid():
            response = response_form.save(commit=False)
            response.user = request.user.userboard
            response.advertisement = advertisement
            response.save()
            author_email = advertisement.author.author.email
            send_response_for_author_email(author_email)
            return redirect('detail', pk=pk)
        
        context = {
            'advertisement': advertisement,
            'responses': responses,
            'response_form': response_form,
        }
        
        return render(request, self.template_name, context)

@login_required
def profile_view(request):
    user_board = request.user.userboard
    advertisements = Advertisement.objects.filter(author=user_board)
    
    responses = UserResponse.objects.filter(advertisement__in=advertisements).order_by('-created_at')
    
    return render(request, 'profile.html', {'responses': responses})

@login_required
def accept_response(request, response_id):
    response = UserResponse.objects.get(pk=response_id)
    if response.advertisement.author == request.user.userboard:
        response.accepted = True
        response.save()
    send_response_email(response.user.author.email)
    return redirect('profile')

@login_required
def delete_response(request, response_id):
    response = UserResponse.objects.get(pk=response_id)
    if response.advertisement.author == request.user.userboard:
        response.delete()
    
    return redirect('profile')