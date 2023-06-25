# импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.shortcuts import render
from .models import Author, Category, Post, PostCategory, Comment
from datetime import datetime
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .filters import PostFilter

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
    ordering = ['-dateCreation']
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(categoryType='AR').order_by('-dateCreation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_count'] = self.get_queryset().count()
        return context


class PostCreateView(CreateView):
    model = Post
    context_object_name = 'new_post'
    template_name = 'create_post.html'
    fields = ('author', 'title', 'text', 'categoryType')
    success_url = reverse_lazy('news')

class PostDeleteView(DeleteView):
    model = Post
    context_object_name = 'delete_post_form'
    template_name = 'post_delete.html'
    fields = ('title', 'dateCreation')
    success_url = reverse_lazy('news')

class PostUpdateView(UpdateView):
    model = Post
    context_object_name = 'edit_post_form'
    template_name = 'post_edit.html'
    fields = ('title', 'text')
    success_url = reverse_lazy(viewname='news')

class NewsDetail(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'

    def get_queryset(self):
        return Post.objects.filter(categoryType='NW')  # показываем только новости


class PostSearch(ListView):
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