from django.contrib import admin
from .models import User, Vendor, Customer, Category, Product, ProductImage, ProductAttribute, Order, OrderItem, Payment, Delivery, Review

# User Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'phone', 'address')
    list_editable = ('role',)
    list_per_page = 20
    list_filter = ('role',)

# Vendor Admin
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user', 'location', 'is_approved')
    list_per_page = 20
    list_filter = ('is_approved', 'location')

# Customer Admin
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'shipping_address', 'billing_address')
    list_per_page = 20
    list_filter = ('user',)

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'parent_category')
    list_per_page = 20
    list_filter = ('name', 'parent_category')

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'vendor', 'is_active')
    list_per_page = 20
    list_filter = ('vendor', 'is_active', 'categories')
    filter_horizontal = ('categories',)  # For easier selection of categories

# ProductImage Admin
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'is_primary')
    list_per_page = 20
    list_filter = ('product', 'is_primary')

# ProductAttribute Admin
@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute_name', 'attribute_value')
    list_per_page = 20
    list_filter = ('product', 'attribute_name')

# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'status', 'created_at')
    list_per_page = 20
    list_filter = ('status', 'created_at')

# OrderItem Admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_per_page = 20
    list_filter = ('order', 'product')

# Payment Admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'payment_method', 'status', 'created_at')
    list_per_page = 20
    list_filter = ('status', 'payment_method')

# Delivery Admin
@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'estimated_delivery_date', 'actual_delivery_date')
    list_per_page = 20
    list_filter = ('status',)

# Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'rating', 'created_at')
    list_per_page = 20
    list_filter = ('rating', 'created_at')