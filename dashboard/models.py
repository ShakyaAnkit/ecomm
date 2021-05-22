from django.db import models
from django.contrib.auth.models import User

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


  

