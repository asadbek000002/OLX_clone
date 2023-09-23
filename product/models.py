from django.db import models


from accounts.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    image = models.ImageField(upload_to='category/images')
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', related_name='childs', on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='categories', blank=True, null=True)

    class Meta:
        ordering = ['name',]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30)
    user = models.ForeignKey(CustomUser, related_name='cities', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='districts')
    user = models.ForeignKey(CustomUser, related_name='districts', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='category')
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='products/images')
    location = models.ForeignKey(District, on_delete=models.PROTECT)
    price = models.IntegerField()
    views_count = models.IntegerField(default=0, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='products')
    is_active = models.BooleanField()
    is_banned = models.BooleanField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['name',]
        verbose_name = 'product'
        verbose_name_plural = 'products'


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def str(self):
        return f"{self.user.name} | {self.product.name}"


class Saved(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='saved')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='saved')
    created_at = models.DateTimeField(auto_now_add=True)


class Ban(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='banfluds')


class Banned(models.Model):
    comment = models.CharField(max_length=250, blank=True, null=True)
    ban = models.ForeignKey(Ban, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bans')

