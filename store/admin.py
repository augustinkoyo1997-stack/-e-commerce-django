# store/admin.py
from django.contrib import admin
from .models import Category, SubCategory, Product, MonthlySales

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'slug')
    list_filter = ('category',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'subcategory', 'price', 'supplier', 'rating', 'is_new', 'sales_count', 'created_at')
    list_filter = ('category', 'subcategory', 'is_new', 'supplier')
    search_fields = ('name', 'supplier', 'description')
    list_editable = ('price', 'is_new', 'sales_count')
    readonly_fields = ('created_at',)
    list_per_page = 20
    fieldsets = (
        ('Informations principales', {
            'fields': ('name', 'slug', 'category', 'subcategory', 'supplier')
        }),
        ('Prix et ventes', {
            'fields': ('price', 'sales_count', 'rating')
        }),
        ('Statut', {
            'fields': ('is_new',)
        }),
        ('Images', {
            'fields': ('image',)
        }),
        ('Dates', {
            'fields': ('created_at',)
        }),
    )
    prepopulated_fields = {'slug': ('name',)}

@admin.register(MonthlySales)
class MonthlySalesAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'month', 'quantity_sold')
    list_filter = ('month', 'product')
    search_fields = ('product__name',)