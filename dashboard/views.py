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

from .models import AuditTrail



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

# Password Reset
class ChangePasswordView(CustomLoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = ChangePasswordForm
    template_name = "dashboard/auth/change_password.html"
    success_message = "Password Has Been Changed"
    success_url = reverse_lazy('dashboard:index')

    def get_form(self):
        form = super().get_form()
        form.set_user(self.request.user)
        return form

    def form_valid(self, form):
        account = User.objects.filter(username=self.request.user).first()
        account.set_password(form.cleaned_data.get('confirm_password'))
        account.save(update_fields=['password'])
        user = authenticate(username=self.request.user, password=form.cleaned_data.get('confirm_password'))
        login(self.request, user)
        return super().form_valid(form)


# AuditTrail List
class AuditTrailListView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, ListView):
    model = AuditTrail
    paginate_by = 100
    template_name = 'dashboard/audittrails/list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-created_at')
