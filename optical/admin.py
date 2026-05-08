from django.contrib import admin
from .models import Inquiry, Product, Testimonial


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price_range', 'is_featured')
    list_filter = ('category', 'is_featured', 'brand')
    search_fields = ('name', 'brand')
    list_editable = ('is_featured',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'rating', 'location', 'is_active', 'created_at')
    list_filter = ('rating', 'is_active')
    list_editable = ('is_active',)