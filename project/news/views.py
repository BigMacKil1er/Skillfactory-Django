# импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
# from django.shortcuts import render
from .models import Author, Category, Post, PostCategory, Comment
from datetime import datetime

class AuthorsList(ListView):
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


class AuthorDetail(DetailView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'author'


class NewsList(ListView):
    model = Post
    template_name = 'newslist.html'
    context_object_name = 'newslist'

    def get_queryset(self):
        return Post.objects.filter(categoryType='NW').order_by('-dateCreation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_count'] = self.get_queryset().count()
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'

    def get_queryset(self):
        return Post.objects.filter(categoryType='NW')  # показываем только новости
