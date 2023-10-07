from django.contrib import admin

from .models import Category, Product, Comment, \
                    City, District, Ban, Banned, Saved


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'description', 'price', 'is_active', 'is_banned', 'updated_at',
                    'is_deleted']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'is_banned', 'is_deleted']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created', 'is_active', 'is_banned']
    list_filter = ['is_active', 'created']
    search_fields = ['user', 'body']


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


@admin.register(Saved)
class SavedAdmin(admin.ModelAdmin):
    list_display = ['product', 'user',]