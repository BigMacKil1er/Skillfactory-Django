from django.urls import path
from .views import LoginView, LogoutView, RegisterView, ConfirmView
app_name = 'accounts'
urlpatterns = [
   path('login/', LoginView.as_view(), name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path('signup/', RegisterView.as_view(), name='signup'),
   path('confirm/<str:confirmation_code>/', ConfirmView.as_view(), name='confirm_registration'),
]