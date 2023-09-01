from django.urls import path
from django.views.decorators.cache import cache_page

from .views import NewsList, NewsDetail, AuthorsList, AuthorDetail, PostSearch, \
    PostCreateView, PostUpdateView, PostDeleteView, PostCategoryView, unsubscribe, upgrade_me, subscribe  # импортируем наше представление

urlpatterns = [
    path('authors/', AuthorsList.as_view()),
    path('authors/<int:pk>', AuthorDetail.as_view()),
    path('news/', NewsList.as_view(), name='news'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('search/', PostSearch.as_view(), name='search'),
    path('create/', PostCreateView.as_view(), name='new_post'),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('news/<int:pk>/deletepost/', PostDeleteView.as_view(), name='delete_post'),
    path('category/<int:pk>', PostCategoryView.as_view(), name='category'),
    path('subscribe/<int:pk>', subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe, name='unsubscribe'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
   
]