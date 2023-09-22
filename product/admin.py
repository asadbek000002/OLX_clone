from django.contrib import admin

from .models import Category, Product, City, District, Ban, Banned



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'description', 'price', 'is_active', 'is_banned', 'updated_at',
                    'is_deleted']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'is_banned', 'is_deleted']


@admin.register(City)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'user']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(District)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'city', 'user']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ban)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'user']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Banned)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['comment', 'ban', 'product', 'user']
