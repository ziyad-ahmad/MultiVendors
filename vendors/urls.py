from django.urls import path
from .views import (
    home, register_user, update_user,
    create_vendor, update_vendor,
    create_customer, update_customer,
    create_product, update_product, category_home, category_product,
    create_order, update_order,
    admin_dashboard, approve_vendor, approve_product,
    vendor_dashboard, customer_dashboard,
    add_to_cart, checkout,cart_view,update_cart, remove_from_cart,category_product,product_detail
)

urlpatterns = [
    # Home Page
    path('', home, name='home'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path("login/", home, name="login"),
    path("logout/", home, name="logout"),
    path('category/<int:category_id>/', category_product, name='category_products'),
    path('category/<int:category_id>/<int:product_id>/', product_detail, name='product_detail'),
    #cart Management
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
    path('customer/cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('customer/checkout/', checkout, name='checkout'),

    # Product URLs
    path('product/create/', create_product, name='create_product'),
    path('product/update/<int:product_id>/', update_product, name='update_product'),
    path('category/', category_home, name='category_home'),
    path('category/<int:pk>/', category_product, name='category_product'),

    # Order URLs
    path('order/create/', create_order, name='create_order'),
    path('order/update/<int:order_id>/', update_order, name='update_order'),

    # Admin URLs
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/approve-vendor/<int:vendor_id>/', approve_vendor, name='approve_vendor'),
    path('admin/approve-product/<int:product_id>/', approve_product, name='approve_product'),
]