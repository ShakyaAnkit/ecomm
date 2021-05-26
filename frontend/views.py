from django.shortcuts import render
from django.views.generic import TemplateView

# Home
class HomeView(TemplateView):
    template_name = 'frontend/layouts/home.html'
