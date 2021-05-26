from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .choices import CUSTOMER_CHOICES, DISCOUNT_CHOICES, GENDER_CHOICES

# Create your models here.

# Audit Log which records transactions
class AuditTrail(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    model_type = models.CharField('Model Type', max_length=255)
    object_id = models.IntegerField('Model Id')
    object_str = models.CharField('Model Str', max_length=255)
    action = models.CharField(max_length=255)
    ip = models.GenericIPAddressField(null=True)
    instance = models.JSONField(null=True)
    previous_instance = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.model_type)


class DateTimeModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
    )
    updated_at = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
    )
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, hard=False):
        if not hard:
            self.deleted_at = timezone.now()
            super().save()
        else:
            return super().delete()


class Brand(DateTimeModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="brands/", null=True, blank=True)
    slug = models.SlugField()

    class Meta:
        ordering = ["name"]
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands' 
    
    def __str__(self):
        return self.name

class Category(DateTimeModel):
    title = models.CharField('Title', max_length=255)
    slug = models.SlugField('Slug')
    description = models.TextField('Description', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='categories')
    image = models.ImageField('Photo', upload_to='images/', null=True, blank=True)

    class Meta:
        ordering = ["title"]
        verbose_name = 'Category'
        verbose_name_plural = 'Categories' 

    def __str__(self):
        return self.title

class Account(DateTimeModel, User):
    customer_type = models.CharField(max_length=100, choices=CUSTOMER_CHOICES, default="Registered")
    gender = models.CharField("Gender", max_length=100, choices=GENDER_CHOICES, default="Male")
    city = models.CharField("City", max_length=255, null=True, blank=True)
    address = models.CharField("Address", max_length=255, null=True, blank=True)
    contact_no = models.PositiveIntegerField("Contact Number")
    billing_addr = models.CharField("Billing Address", max_length=255, default=" ")
    shipping_addr = models.CharField("Shipping Address", max_length=255, default=" ")
    cart_items = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = 'Category'
        verbose_name_plural = 'Categories' 

    def __str__(self):
        return self.username

class Coupon(DateTimeModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField("Coupon Title", max_length=255)
    code = models.CharField("Coupon Code", max_length=255)
    valid_from = models.DateTimeField("Valid From")
    valid_to = models.DateTimeField("Valid To")
    validity_count = models.PositiveIntegerField("Validity Count", null=True, blank=True, default=1)
    discount_type = models.PositiveIntegerField("Discount Type", choices=DISCOUNT_CHOICES, default=1)
    discount_percent = models.FloatField("Discount Percentage", default=0)
    discount_amount = models.FloatField("Discount Amount", default=0)
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ["title"]
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons' 

    def __str__(self):
        return self.title
