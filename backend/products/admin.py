from django.contrib import admin
from django.utils.html import format_html
from .models import Category, CoffeeProduct

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'

@admin.register(CoffeeProduct)
class CoffeeProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'price', 'stock', 'is_available', 'image_preview']
    list_filter = ['region', 'process', 'roast_level', 'is_available', 'is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'slug', 'description', 'category')
        }),
        ('Coffee Details', {
            'fields': ('region', 'process', 'roast_level')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'weight', 'stock', 'is_available', 'is_featured')
        }),
        ('Images', {
            'fields': ('main_image', 'image_preview', 'image_2', 'image_3')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.main_image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'