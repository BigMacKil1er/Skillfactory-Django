from django.urls import path
from .views import CreateAdvertisement, PostList, AdvertisementDetail, AdvertisementDetailUpdate, AdvertisementDelete, AdvertisementResponseView, accept_response, delete_response, profile_view
urlpatterns = [
    path('', PostList.as_view(), name="home"),
    path('create/', CreateAdvertisement.as_view()),
    path('<int:pk>', AdvertisementDetail.as_view(), name='detail'),
    path('<int:pk>/edit', AdvertisementDetailUpdate.as_view(), name='edit'),
    path('<int:pk>/delete/', AdvertisementDelete.as_view(), name='delete'),
    path('<int:pk>/response/', AdvertisementResponseView.as_view(), name='response'),
    path('profile/', profile_view, name='profile'),
    path('accept_response/<int:response_id>/', accept_response, name='accept_response'),
    path('delete_response/<int:response_id>/', delete_response, name='delete_response'),
]
