from django.db import models

# Create your models here.

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


  

