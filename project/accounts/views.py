from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from .forms import RegisterForm, LoginForm

class RegisterView(CreateView):
   model = User
   form_class = RegisterForm
   template_name = 'registration/register.html'
   success_url = '/news'
   def form_valid(self, form):
       user = form.save()
       # group = Group.objects.get(name='my_group') # Обращаемся к БД, находим нужную группу. Может оказаться, что такой группы в БД нет. Тогда получим ошибку. Надёжнее использовать метод get_or_create. Обратите внимание, что этот метод возвращает кортеж, поэтому мы обращаемся к первому элементу кортежа через скобки.
    #    group = Group.objects.get_or_create(name='common')[0]
    #    user.groups.add(group)
       user.save()
       return super().form_valid(form)

class LoginView(FormView):
   model = User
   form_class = LoginForm
   template_name = 'registration/login.html'
   success_url = '/news'
  
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