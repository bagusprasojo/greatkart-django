from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count
from django.template.defaultfilters import slugify
from colorfield.fields import ColorField

# Create your models here.




class MyColor(models.Model):
    color_hexa  = ColorField(default='#FF0000', unique=True)
    color_name  = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.color_name

# class ProductColor(models.Model):
#     color_name = models.CharField(max_length=20, unique=True)
#     color_hexa = models.CharField(max_length=20, unique=True)

class Product(models.Model):
    product_name        = models.CharField(max_length=200, unique=True)
    slug                = models.SlugField(max_length=200, unique=True)
    product_description = models.TextField(max_length=255, blank=True)
    price               = models.IntegerField()
    image               = models.ImageField(upload_to='photos/product')
    stock               = models.IntegerField()
    is_available        = models.BooleanField(default=True)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date        = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)
    user                = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('products_detail',args=[self.category.slug, self.slug])

    def averageRating(self):
        reviews = ReviewRating.objects.filter(status=True, product  = self).aggregate(average = Avg('rating'))
        avg = 0

        if reviews['average'] is not None:
            avg = float(reviews['average'])

        return avg

    def averageCount(self):
        reviews = ReviewRating.objects.filter(status=True, product  = self).aggregate(count = Count('rating'))
        count = 0

        if reviews['count'] is not None:
            count = float(reviews['count'])

        return count



    def save(self, *args, **kwargs):
        if not self.price:
            self.price = 90

        if not self.stock:
            self.stock = 1000

        if not self.slug:
            self.slug = slugify(self.product_name)


        super().save(*args, **kwargs);

variation_category_choice = (
    ('color','color'),
    ('size','size'),
    ('model','model'),
)

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size', is_active=True)

    def models(self):
        return super(VariationManager,self).filter(variation_category='model', is_active=True)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)

    objects = VariationManager()
    def __str__(self):
        return self.variation_value

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class ProductGalery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to="store/products/", max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgalery'
        verbose_name_plural = 'product galeries'
