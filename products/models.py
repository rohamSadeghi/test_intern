from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


def product_images_path(instance, filename):
    return f'products/{instance.id}-{filename}'

class EnableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_enable=True)


class ParentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(parent__isnull=True)


class Store(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="owner", on_delete=models.CASCADE)
    is_enable = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    phone_number = models.BigIntegerField(unique=True)
    address = models.TextField(blank=True)

    products = models.ManyToManyField('Product', related_name='stores')

    class Meta:
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')

    def __str__(self):
        return self.name


class Category(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='children')
    properties = JSONField(default=dict)
    is_enable = models.BooleanField(default=True)

    objects = models.Manager()
    parents = ParentManager()

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def clean(self):
        super().clean()
        if self.parent and self == self.parent.parent:
            raise ValidationError(_("This category is somehow a child category and can not be parent again"))

    def __str__(self):
        return self.name


class Product(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rating = None

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to=product_images_path)
    is_enable = models.BooleanField(default=True)
    properties = JSONField(default=dict)

    categories = models.ManyToManyField('Category', related_name='products')

    objects = models.Manager()
    enables = EnableManager()

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        old_image = ''
        if self.image:
            old_image = self.image
            self.image = ''
            super().save(*args, **kwargs)
        self.image = old_image
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})

    def rating(self):
        if self._rating is None:
            self._rating = ProductRating.objects.filter(
                product=self
            ).aggregate(
                avg_rating=Coalesce(models.Avg('rate'), 0),
                rating_count=models.Count('id')
            )
        return self._rating

    def rating_avg(self):
        return self.rating()['avg_rating']

    def rating_count(self):
        return self.rating()['rating_count']


class ProductRating(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='rates')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rates')

    class Meta:
        verbose_name = _('Product rating')
        verbose_name_plural = _('Product ratings')
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_product_user')
            ]

    def __str__(self):
        return f"user: {self.user}->product{self.product}"

    def get_absolute_url(self):
        return reverse('products-list')


class ProductBookmark(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    like_status = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Product bookmark')
        verbose_name_plural = _('Product bookmarks')
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_product_user_bookmark')
            ]
