from django.contrib import admin
from .models import Product, Category, Order

# Register your models here.
@admin.register(Product)
class productAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'is_available', 'category', 'stock', 'created_at']
    search_fields = ['name', 'price', 'is_available', 'category', 'created_at']
    list_filter = ['price', 'is_available', 'category', 'created_at']

@admin.register(Category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']

@admin.register(Order)
class orderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'address', 'total_price', 'status', 'created_at']
    search_fields = ['full_name', 'phone', 'address', 'status', 'created_at']
    list_filter = ['address', 'status', 'created_at']