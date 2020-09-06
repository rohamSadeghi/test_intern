from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.functions import Coalesce
from django.urls import reverse


def product_images_path(instance, filename):
    return f'products/{instance.id}-{filename}'

class EnableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_enable=True)

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

    def __str__(self):
        return self.name


class Category(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='categories')
    is_enable = models.BooleanField(default=True)

    def clean(self):
        super().clean()
        if self.parent and self == self.parent.parent:
            raise ValidationError("This category is somehow a child category and can not be parent again")

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
    objects = models.Manager()
    enables = EnableManager()

    categories = models.ManyToManyField('Category', related_name='products')

    def __str__(self):
        return self.name

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
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
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
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_product_user_bookmark')
            ]
