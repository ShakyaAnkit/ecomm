from django.urls import path

from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('accounts/login/', LoginPageView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout')
]