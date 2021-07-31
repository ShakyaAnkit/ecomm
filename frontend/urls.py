from django.urls import path, include

from . import views

app_name="frontend"

urlpatterns = [
   path('', views.HomeView.as_view(), name='home'),
   path('login/', views.LoginView.as_view(), name='login'),
   path('register/', views.SignUpView.as_view(), name='register'),
]