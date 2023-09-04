from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Advertisement
# Create your views here.
class PostList(ListView):
    model = Advertisement
    template_name = 'post_list.html'
    context_object_name = 'postlist'
    ordering = ['-date_creation']
    paginate_by = 10
