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
    list_display = ('name', 'slug', 'parent_category')
    list_per_page = 20
    list_filter = ('name', 'parent_category')


# ProductImage Admin
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # Number of empty forms to display

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 2  # Number of empty forms to display

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductAttributeInline]
    list_display = ('name', 'vendor', 'price', 'is_active', 'is_featured')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'is_featured', 'categories')

    def save_model(self, request, obj, form, change):
        # Save the Product instance first to generate a primary key
        super().save_model(request, obj, form, change)
        
        # Now you can set related fields (e.g., ProductImage, ProductAttribute)
        # This is handled automatically by the inlines
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
    list_display = ('id', 'customer', 'get_product', 'rating', 'created_at')
    list_per_page = 20
    list_filter = ('rating', 'created_at')

    def get_product(self, obj):
        return ", ".join([product.name for product in obj.reviews_product.all()])
    get_product.short_description = 'Product'