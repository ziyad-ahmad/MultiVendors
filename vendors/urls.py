from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    genHome, register_user, update_user,
    create_vendor, update_vendor,
    create_customer, update_customer,
    create_product, update_product, category_home, 
    create_order, update_order,
    admin_dashboard, admin_vendor_management, 
    vendor_dashboard, customer_dashboard,
    add_to_cart, checkout, cart_view, update_cart, remove_from_cart, product_detail
)

urlpatterns = [
    # Home Page
    path('', genHome, name='genHome'),  # General home page
    path('home/', category_home, name='category_home'),  # Display all products
    path('category/<int:category_id>/', category_home, name='category_product'),  # Display products by category
    path('product/<int:product_id>/', product_detail, name='product_detail'),

    # Cart Management
    path('cart/', cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),

    # User Authentication
    path('register/', register_user, name='register_user'),
    path('update/<int:user_id>/', update_user, name='update_user'),

    # Vendor URLs
    path('vendor/create/', create_vendor, name='create_vendor'),
    path('vendor/update/<int:vendor_id>/', update_vendor, name='update_vendor'),
    path('vendor/dashboard/', vendor_dashboard, name='vendor_dashboard'),

    # Customer URLs
    path('customer/create/', create_customer, name='create_customer'),
    path('customer/update/<int:customer_id>/', update_customer, name='update_customer'),
    path('customer/dashboard/', customer_dashboard, name='customer_dashboard'),

    # Product URLs
    path('product/create/', create_product, name='create_product'),
    path('product/update/<int:product_id>/', update_product, name='update_product'),

    # Order URLs
    path('order/create/', create_order, name='create_order'),
    path('order/update/<int:order_id>/', update_order, name='update_order'),

    # Admin URLs
    path('admins/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admins/vendor-management/', admin_vendor_management, name='admin_vendor_management'),
    # Static and Media Files
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)