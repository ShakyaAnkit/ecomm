import subprocess

from django.conf import settings as conf_settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import resolve, reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import View, TemplateView, FormView, ListView, CreateView, UpdateView, DeleteView

from .audits import store_audit

from .forms import (
    ChangePasswordForm, 
    LoginForm, 
)

from .mixins import (
    BaseMixin, 
    AuditCreateMixin, 
    AuditUpdateMixin, 
    AuditDeleteMixin, 
    CustomLoginRequiredMixin, 
    GetDeleteMixin, 
    GroupRequiredMixin,
    NonDeletedListMixin, 
    NonLoginRequiredMixin, 
    NonSuperAdminRequiredMixin, 
    SuperAdminRequiredMixin
)



# Create your views here.
class DashboardView(CustomLoginRequiredMixin, TemplateView):
    template_name = "dashboard/layouts/home.html"


# Login Logout Views
class LoginPageView(NonLoginRequiredMixin, FormView):
    form_class = LoginForm
    template_name = "dashboard/auth/login.html"

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        # Remember me
        if self.request.POST.get('remember', None) == None:
            self.request.session.set_expiry(0)

        login(self.request, user)
        store_audit(request= self.request, instance=self.request.user, action='LOGIN')

        if 'next' in self.request.GET:
            return redirect(self.request.GET.get('next'))
        return redirect('dashboard:home')

class LogoutView(CustomLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        store_audit(request= self.request, instance=self.request.user, action='LOGOUT')
        logout(request)
        return redirect('dashboard:login')
