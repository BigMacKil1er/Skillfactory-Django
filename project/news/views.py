# импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from typing import Any, Dict
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

# from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .forms import SubscribeForm
from .models import Author, Category, Post, PostCategory, Comment
from datetime import datetime
from django.core.paginator import Paginator
from django.urls import resolve, reverse_lazy
from .filters import PostFilter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL

class AuthorsList(LoginRequiredMixin, ListView):
    model = Author
    template_name = 'authors.html'
    context_object_name = 'authors'

    def get_queryset(self):

        return Author.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        return context



class AuthorDetail(LoginRequiredMixin, DetailView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'author'


class NewsList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'newslist.html'
    context_object_name = 'newslist'
    ordering = ['-dateCreation']
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(categoryType='NW').order_by('-dateCreation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_count'] = self.get_queryset().count()
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


# def get_users_with_edit_permission():
#     content_type = ContentType.objects.get_for_model(Post)
#     edit_post_permission = Permission.objects.create(
#         codename='authors',
#         name='Authors',
#         content_type = content_type
#     )

#     # Получаем всех пользователей, которые имеют право на редактирование постов
#     users_with_edit_permission = User.objects.filter(user_permissions=edit_post_permission)
    
#     return users_with_edit_permission

class PostCategoryView(DetailView):
    model = Post
    template_name = 'category.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10
    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        c = Category.objects.get(id=self.id)
        querySet = Post.objects.filter(postCategory=c)
        # print(querySet)
        return querySet
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.get(id=self.id)
        print(user)
        subscribed = category.subscribers.filter(email=user.email)
        print(subscribed)
        if not subscribed:
            context['category'] = category
        return context

class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('auth.authors')
    model = Post
    context_object_name = 'new_post'
    template_name = 'create_post.html'
    fields = ('author', 'title', 'text', 'categoryType', 'postCategory')
    success_url = reverse_lazy('news')

    @staticmethod
    def send_message(username, email, title, text):
        html_email_message = render_to_string('new_post_email_notification.html', {'username': username, 'title': title,'text': text})
        msg = EmailMultiAlternatives(
            subject=title,
            body=text,
            from_email='artjom.varibrus@yandex.ru',
            to=[email]
        )
        msg.attach_alternative(html_email_message, 'text/html')
        try:
            msg.send()
        except:
            print('Спам')


class PostDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('auth.authors')
    model = Post
    context_object_name = 'delete_post_form'
    template_name = 'post_delete.html'
    fields = ('title', 'dateCreation')
    success_url = reverse_lazy('news')

class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('auth.authors')
    model = Post
    context_object_name = 'edit_post_form'
    template_name = 'post_edit.html'
    fields = ('title', 'text')
    success_url = reverse_lazy(viewname='news')


class NewsDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news_d'

    def get_queryset(self):
        return Post.objects.filter(categoryType='NW')  # показываем только новости
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        cache_key = f'post_{pk}'
        cached_post = cache.get(cache_key)
        if cached_post is None:
            post = get_object_or_404(Post.objects.filter(categoryType='NW'), pk=pk)
            cache.set(cache_key, post)
            return post
        else:
            return cached_post

class PostSearch(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'newslist'
    ordering = ['-dateCreation']
    paginate_by = 10

    def get_queryset(self):
        filtered_queryset = PostFilter(self.request.GET, queryset=Post.objects.filter(categoryType='NW')).qs
        return filtered_queryset.order_by('-dateCreation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['newslist'] = page_obj
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

@login_required
def upgrade_me(request):
   user = request.user
   premium_group = Group.objects.get(name='authors')
   if not request.user.groups.filter(name='authors').exists():
       premium_group.user_set.add(user)
       Author.objects.create(authorUser=user)
       premium_group.save()
   return redirect('/news')

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    print(DEFAULT_FROM_EMAIL)
    if not category.subscribers.filter(id=user.id).exists():
        print('here2')
        email = user.email
        category.subscribers.add(user)
        html = render_to_string(
            template_name='new_post_email_notification.html',
            context={
                'categories': category,
                'user': user
            }
        )
        print(html)
        msg = EmailMultiAlternatives(
            subject=f'{category} subscription',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=[email,]
        )
        msg.attach_alternative(html, 'text/html')
        try:
            msg.send()
        except Exception as e:
            print(e)
        return redirect('/news')
    
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def unsubscribe(request, pk):
    user = request.user
    c = Category.objects.get(id=pk)
    if c.subscribers.filter(id=user.id).exists():
        c.subscribers.remove(user)
    return redirect('/about')