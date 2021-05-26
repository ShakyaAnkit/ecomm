from django.contrib.auth.models import Group, User
from django import forms
from django.utils.html import mark_safe

from .mixins import FormControlMixin 
from .models import Brand, Category, Coupon

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder':  'Username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder':  'Password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = User.objects.filter(username=username, is_active=True).first()
        if user == None or not user.check_password(password):
            for field in self.fields:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control error-input'
                })
            raise forms.ValidationError(
                {"username":"Incorrect username or password"}
            )
        return self.cleaned_data

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder':  'Current Password'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder':  'Password'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder':  'Confirm Password'}))

    def set_user(self, user):
        self.user = user
    
    def clean(self):
        current_password = self.cleaned_data.get('current_password')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
    
        if not self.user.check_password(current_password):
            raise forms.ValidationError({"current_password": "Incorrect current password" })
        if password != confirm_password:
            raise forms.ValidationError({'confirm_password': "Password confirmation failed" })

        return self.cleaned_data


class UserForm(FormControlMixin, forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'groups']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].widget.attrs.update({
            'class': 'form-control select2'
        })
        self.fields['email'].required = True
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("User with this email address already exists")
        
        return email


class BrandForm(FormControlMixin, forms.ModelForm):

    class Meta:
        model = Brand
        fields = ['name', 'slug', 'image']
    

class CategoryForm(FormControlMixin, forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['title','slug','description','parent', 'image']
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if Category.objects.filter(deleted_at__isnull=True, slug=slug).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Category with this Slug already exists.")
        else:
            return slug

class CouponForm(FormControlMixin, forms.ModelForm):
    
    class Meta:
        model = Coupon
        fields = '__all__'
