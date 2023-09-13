from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView

from callboard.models import UserBoard
from .models import Registration
from mmorpg.tasks.User_greeting import send_confirmation_email

from mmorpg.tasks.User_greeting import greeting
from .forms import RegisterForm, LoginForm
from django.utils.crypto import get_random_string

class RegisterView(CreateView):
   model = User
   form_class = RegisterForm
   template_name = 'registration/register.html'
   success_url = '/accounts/login'
   def form_valid(self, form):
       user = form.save()
       confirmation_code = get_random_string(length=32)
       registration = Registration.objects.create(user=user, confirmation_code=confirmation_code)
       registration.save()
       group = Group.objects.get_or_create(name='common')[0]
       group_2 = Group.objects.get_or_create(name='Authors')[0]
       user.groups.add(group,group_2)
       user.is_active = False
       UserBoard.objects.get_or_create(author=self.request.user)
       user.save()
    #    greeting(user)
       send_confirmation_email(user.email, confirmation_code)
       print('done')
       return super().form_valid(form)

class ConfirmView(DetailView):
    def get(self, request, confirmation_code):
        try:
            registration = Registration.objects.get(confirmation_code=confirmation_code, is_confirmed=False)
            registration.user.is_active = True
            registration.user.save()
            registration.is_confirmed = True
            registration.save()
            return render(request, 'registration/confirmation_success.html')
        except Registration.DoesNotExist:
            return render(request, 'registration/confirmation_error.html')

class LoginView(FormView):
   model = User
   form_class = LoginForm
   template_name = 'registration/login.html'
   success_url = '/'
  
   def form_valid(self, form):
       username = form.cleaned_data.get('username')
       password = form.cleaned_data.get('password')
       user = authenticate(self.request,username=username, password=password)
       if user is not None:
           login(self.request, user)
       return super().form_valid(form)
  
  
class LogoutView(TemplateView):
   template_name = 'registration/logout.html'
  
   def get(self, request, *args, **kwargs):
       logout(request)
       return super().get(request, *args, **kwargs)
   
