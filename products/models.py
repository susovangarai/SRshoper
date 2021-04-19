import random
import string
from pathlib import Path
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from ecommerce.utils import unique_slug_generator


def get_filename(filepath):
    name = Path(filepath).name
    ext = Path(filepath).suffix
    return name, ext


def image_upload_path(instance, filename):
    name, ext = get_filename(filename)
    return "products/" + "".join(
        random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(15)) + ext


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=19, decimal_places=2)
    image = models.ImageField(upload_to=image_upload_path, default=None, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return ''


@receiver(pre_save, sender=Product)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
