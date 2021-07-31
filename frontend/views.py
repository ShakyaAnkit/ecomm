from django.shortcuts import render
from django.views.generic import TemplateView

# Home
class HomeView(TemplateView):
    template_name = 'frontend/layouts/home.html'

class LoginView(TemplateView):
    template_name = 'frontend/layouts/login.html'

class SignUpView(TemplateView):
    template_name = 'frontend/layouts/register.html'
