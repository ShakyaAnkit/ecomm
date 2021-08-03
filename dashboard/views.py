import subprocess

from django.conf import settings as conf_settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import resolve, reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import View, TemplateView, FormView, ListView, CreateView, UpdateView, DeleteView

from .audits import store_audit

from .forms import (
    BrandForm,
    CategoryForm,
    ChangePasswordForm, 
    CouponForm,
    LoginForm, 
    ProductForm,
    SizeForm,
    VariantFormSet, 
)

from .mixins import (
    ActiveMixin,
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

from .models import Account, AuditTrail, Brand, Category, Coupon, Product, Size, Variants



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
class AuditTrailListView(CustomLoginRequiredMixin, ActiveMixin, SuperAdminRequiredMixin, ListView):
    model = AuditTrail
    paginate_by = 100
    template_name = 'dashboard/audittrails/list.html'
    menu_active = 'audit'
    ordering = ['-created_at']

class SampleListView(TemplateView):
    template_name = 'dashboard/sample/list.html'

class SampleFormView(TemplateView):
    template_name = 'dashboard/sample/form.html'


# Brand CRUD
class BrandListView(CustomLoginRequiredMixin, ActiveMixin, NonDeletedListMixin, ListView):
    model = Brand
    template_name = "dashboard/brands/list.html"
    menu_active = 'brand'


class BrandCreateView(CustomLoginRequiredMixin, ActiveMixin, SuccessMessageMixin, AuditCreateMixin, CreateView):
    model = Brand
    template_name = "dashboard/brands/form.html"
    form_class = BrandForm
    success_url = reverse_lazy("dashboard:brands-list")
    success_message = "Brand has been Created Successfully"
    menu_active = 'brand'


class BrandUpdateView(CustomLoginRequiredMixin, ActiveMixin, SuccessMessageMixin, AuditUpdateMixin, UpdateView):
    model = Brand
    template_name = "dashboard/brands/form.html"
    form_class = BrandForm
    success_url = reverse_lazy("dashboard:brands-list")
    success_message = "Brand has been Updated Successfully"
    menu_active = 'brand'


class BrandDeleteView(CustomLoginRequiredMixin, AuditDeleteMixin, GetDeleteMixin, DeleteView):
    model = Brand
    template_name = "dashboard/brands/delete.html"
    success_url = reverse_lazy("dashboard:brands-list")
    success_message = "Brand has been Deleted Successfully"


# Category
class CategoryListView(CustomLoginRequiredMixin, ActiveMixin, NonDeletedListMixin, ListView):
    model = Category
    template_name = "dashboard/category/list.html"
    menu_active = 'category'


class CategoryCreate(CustomLoginRequiredMixin, ActiveMixin, BaseMixin, SuccessMessageMixin, CreateView):
    template_name = "dashboard/category/form.html"
    form_class = CategoryForm
    model = Category
    success_url = reverse_lazy("dashboard:category-list")
    success_message = "Category Created Successfully"
    menu_active = 'category'

class CategoryUpdateView(CustomLoginRequiredMixin, ActiveMixin, SuccessMessageMixin, AuditUpdateMixin, UpdateView):
    model = Category
    template_name = "dashboard/category/form.html"
    form_class = CategoryForm
    success_url = reverse_lazy("dashboard:category-list")
    success_message = "Category has been Updated Successfully"
    menu_active = 'category'

class CategoryDeleteView(CustomLoginRequiredMixin, AuditDeleteMixin, GetDeleteMixin, DeleteView):
    model = Category
    template_name = "dashboard/category/delete.html"
    success_url = reverse_lazy("dashboard:category-list")
    success_message = "Category has been Deleted Successfully"


# User CRUD
class AccountListView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, ListView):
    model = Account
    template_name = "dashboard/accounts/list.html"
    paginate_by = 100
    menu_active = 'account'

    def get_queryset(self):
        return super().get_queryset().exclude(username=self.request.user)

# class UserCreateView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, SuccessMessageMixin, AuditCreateMixin, CreateView):
#     form_class= UserForm
#     success_message = "User Created Successfully"
#     success_url = reverse_lazy('dashboard:users-list')
#     template_name = "dashboard/users/form.html"

#     def get_success_url(self):
#         return reverse('dashboard:users-password-reset', kwargs={'pk': self.object.pk })
    

# class UserUpdateView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, SuccessMessageMixin, AuditUpdateMixin, UpdateView):
#     form_class = UserForm
#     model = User
#     success_message = "User Updated Successfully"
#     success_url = reverse_lazy('dashboard:users-list')
#     template_name = "dashboard/users/form.html"

# class UserStatusView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, SuccessMessageMixin, View):
#     model = User
#     success_message = "User's Status Has Been Changed"
#     success_url = reverse_lazy('dashboard:users-list')

#     def get(self, request, *args, **kwargs):
#         user_id = self.kwargs.get('pk')
#         if user_id:
#             account = User.objects.filter(pk=user_id).first()
#             if account.is_active == True:
#                 account.is_active = False
#             else:
#                 account.is_active = True
#             account.save(update_fields=['is_active'])
#         return redirect(self.success_url)


# # Password Reset
# class UserPasswordResetView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, SuccessMessageMixin, View):
#     model = User
#     success_url = reverse_lazy("dashboard:users-list")
#     success_message = "Password has been sent to the user's email."

#     def get(self, request, *args, **kwargs):
#         user_pk = self.kwargs.get('pk')
#         account = User.objects.filter(pk=user_pk).first()
#         password = get_random_string(length=6)
#         account.set_password(password)
#         msg = (
#             "You can login into the Dashboard with the following credentials.\n\n" + "Username: " + account.username + " \n" + "Password: " + password
#         )
#         send_mail("Dashboard Credentials", msg, conf_settings.EMAIL_HOST_USER, [account.email], fail_silently=True)
#         account.save(update_fields=["password"])

#         messages.success(self.request, self.success_message)
#         return redirect(self.success_url)



# Coupon
class CouponListView(CustomLoginRequiredMixin, ActiveMixin, NonDeletedListMixin, ListView):
    model = Coupon
    template_name = "dashboard/coupons/list.html"
    menu_active = 'coupon'

class CouponCreate(CustomLoginRequiredMixin, ActiveMixin, BaseMixin, SuccessMessageMixin, CreateView):
    template_name = "dashboard/coupons/form.html"
    form_class = CouponForm
    model = Coupon
    success_url = reverse_lazy("dashboard:coupons-list")
    success_message = "Coupon Created Successfully"
    menu_active = 'coupon'

class CouponUpdateView(CustomLoginRequiredMixin, ActiveMixin, SuccessMessageMixin, AuditUpdateMixin, UpdateView):
    model = Coupon
    template_name = "dashboard/coupons/form.html"
    form_class = CouponForm
    success_url = reverse_lazy("dashboard:coupons-list")
    success_message = "Coupon has been Updated Successfully"
    menu_active = 'Coupon'

class CouponDeleteView(CustomLoginRequiredMixin, AuditDeleteMixin, GetDeleteMixin, DeleteView):
    model = Coupon
    template_name = "dashboard/coupons/delete.html"
    success_url = reverse_lazy("dashboard:coupons-list")
    success_message = "Coupon has been Deleted Successfully"

# Size
class SizeListView(CustomLoginRequiredMixin, ActiveMixin, NonDeletedListMixin, ListView):
    model = Size
    template_name = "dashboard/sizes/list.html"
    menu_active = 'size'


class SizeCreateView(CustomLoginRequiredMixin, ActiveMixin, BaseMixin, SuccessMessageMixin, CreateView):
    template_name = "dashboard/sizes/form.html"
    form_class = SizeForm
    success_url = reverse_lazy("dashboard:sizes-list")
    success_message = "Size Created Successfully"
    menu_active = 'size'

class SizeUpdateView(CustomLoginRequiredMixin, ActiveMixin, SuccessMessageMixin, AuditUpdateMixin, UpdateView):
    model = Size
    template_name = "dashboard/sizes/form.html"
    form_class = SizeForm
    success_url = reverse_lazy("dashboard:sizes-list")
    success_message = "Size has been Updated Successfully"
    menu_active = 'size'

class SizeDeleteView(CustomLoginRequiredMixin, AuditDeleteMixin, GetDeleteMixin, DeleteView):
    model = Size
    template_name = "dashboard/sizes/delete.html"
    success_url = reverse_lazy("dashboard:sizes-list")
    success_message = "Size has been Deleted Successfully"

# class CouponCreate(CustomLoginRequiredMixin, ActiveMixin, BaseMixin, SuccessMessageMixin, CreateView):
#     template_name = "dashboard/coupons/form.html"
#     form_class = CouponForm
#     model = Coupon
#     success_url = reverse_lazy("dashboard:coupons-list")
#     success_message = "Coupon Created Successfully"
#     menu_active = 'coupon'

# class CouponUpdateView(CustomLoginRequiredMixin, ActiveMixin, SuccessMessageMixin, AuditUpdateMixin, UpdateView):
#     model = Coupon
#     template_name = "dashboard/coupons/form.html"
#     form_class = CouponForm
#     success_url = reverse_lazy("dashboard:coupons-list")
#     success_message = "Coupon has been Updated Successfully"
#     menu_active = 'Coupon'

# class CouponDeleteView(CustomLoginRequiredMixin, AuditDeleteMixin, GetDeleteMixin, DeleteView):
#     model = Coupon
#     template_name = "dashboard/coupons/delete.html"
#     success_url = reverse_lazy("dashboard:coupons-list")
#     success_message = "Coupon has been Deleted Successfully"


# Product CRUD
class ProductFormsetMixin:
    def get_formset(self):
        if self.request.POST:
            return VariantFormSet(self.request.POST, queryset= Variants.objects.filter(product=self.kwargs.get('pk'), deleted_at__isnull=True), prefix='variants')
        else:
            return VariantFormSet(queryset= Variants.objects.filter(product=self.kwargs.get('pk'), deleted_at__isnull=True), prefix='variants')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['formset'] = self.get_formset()
        return context
    
class ProductListView(CustomLoginRequiredMixin, ActiveMixin, NonDeletedListMixin, ListView):
    model = Product
    template_name = "dashboard/products/list.html"
    menu_active = 'product'
    paginate_by = 100

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

class ProductCreateView(CustomLoginRequiredMixin, ActiveMixin, SuccessMessageMixin, AuditCreateMixin, ProductFormsetMixin, CreateView):
    form_class = ProductForm
    template_name = 'dashboard/products/form.html'
    success_url = reverse_lazy('dashboard:products-list')
    menu_active = 'product'

    def form_valid(self, form):
        context  = self.get_context_data()
        variants = self.get_formset()
        with transaction.atomic():
            self.object = form.save()
            if variants.is_valid():
                for variant in variants:
                    variant.instance.product = self.object
                    variant.save()
            else:
                print(variants.errors)

        return super().form_valid(form)

class ProductUpdateView(CustomLoginRequiredMixin, ActiveMixin, SuccessMessageMixin, AuditUpdateMixin, ProductFormsetMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'dashboard/products/form.html'
    success_url = reverse_lazy('dashboard:products-list')
    menu_active = 'product'

    def form_valid(self, form):
        context  = self.get_context_data()
        variants = self.get_formset()

        with transaction.atomic():
            self.object = form.save()
            if variants.is_valid():
                mark_form = variants.save(commit=False)
                # deleting formset
                for obj in variants.deleted_objects:
                    obj.delete()
                   
                for mark in mark_form:
                    mark.student = self.object
                    mark.save()
              
            else:
                print(variants.errors)   
        return super().form_valid(form)

class ProductDeleteView(CustomLoginRequiredMixin, NonDeletedListMixin, SuccessMessageMixin, GetDeleteMixin, AuditDeleteMixin, DeleteView):
    model = Product
    success_message = "Product Deleted Successfully"
    success_url = reverse_lazy('dashboard:products-list')