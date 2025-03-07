from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('vendor', 'Vendor'),
        ('customer', 'Customer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name="custom_user_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name="custom_user_permissions",
        related_query_name="user",
    )

    def __str__(self):
        return self.username


class Vendor(models.Model):
    STATUS_CHOICE = [
        ('pending', 'Pending'),  # Actual value: 'pending', Display name: 'Pending'
        ('approved', 'Approved'),  # Actual value: 'approved', Display name: 'Approved'
        ('rejected', 'Rejected'),  # Actual value: 'rejected', Display name: 'Rejected'
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor')
    store_name = models.CharField(max_length=100)
    business_details = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICE, default='pending')  # Renamed to 'status'
    is_approved = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.store_name

    def approve_vendor(self):
        """Approve the vendor."""
        self.is_approved = True
        self.status = 'approved'  
        self.save()

    def reject_vendor(self):
        """Reject the vendor."""
        self.is_approved = False
        self.status = 'rejected'  
        self.save()

class VendorDocument(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='vendor_documents/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Document for {self.vendor.store_name}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    shipping_address = models.TextField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    loyalty_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, default='default-category')
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)  # Updated
    updated_at = models.DateTimeField(default=timezone.now)  # Updated

    def __str__(self):
        return self.name + ' - ' + self.slug

class Product(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    sluge = models.SlugField(max_length=255, unique=True, default='product_name')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    sku = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    rating = models.ManyToManyField('Review', related_name='products', through='ReviewProduct')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField('Category', related_name='products')

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    attribute_name = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.attribute_name}: {self.attribute_value} for {self.product.name}"
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)  # Updated
    updated_at = models.DateTimeField(default=timezone.now)  # Updated

    def __str__(self):
        return f"Order #{self.id} by {self.customer.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)  # Updated
    updated_at = models.DateTimeField(default=timezone.now)  # Updated

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('chapipay', 'Chapipay'),
        ('telebir', 'Telebir'),
        ('credit_card', 'Credit Card'),
        ('mobile_money', 'Mobile Money'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  # Updated
    updated_at = models.DateTimeField(default=timezone.now)  # Updated

    def __str__(self):
        return f"Payment for Order #{self.order.id}"


class Delivery(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    delivery_person = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    estimated_delivery_date = models.DateField(blank=True, null=True)
    actual_delivery_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  # Updated
    updated_at = models.DateTimeField(default=timezone.now)  # Updated

    def __str__(self):
        return f"Delivery for Order #{self.order.id}"

class Review(models.Model):
    customer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField(default='')
    rating = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)

    def clean(self):
        """
        Validate that the rating is between 1 and 5.
        """
        if self.rating < 1 or self.rating > 5:
            raise ValidationError({'rating': 'Rating must be between 1 and 5.'})

    def __str__(self):
        return f"Review by {self.customer}"
    
class ReviewProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews_product')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reviews_product', default=0)  # Add default value
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.review.customer} for {self.product.name}"