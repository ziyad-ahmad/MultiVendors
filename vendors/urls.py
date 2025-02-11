from django.urls import path
from .views import register_user, update_user,create_vendor, update_vendor,create_order, home
from .views import create_customer, update_customer, create_product, update_product,update_order
urlpatterns = [
    path('', home, name='home'),
    path('register/', register_user, name='register_user'),
    path('update/<int:user_id>/', update_user, name='update_user'),
    path('vendor/create/', create_vendor, name='create_vendor'),
    path('vendor/update/<int:vendor_id>/', update_vendor, name='update_vendor'),
    path('customer/create/', create_customer, name='create_customer'),
    path('customer/update/<int:customer_id>/', update_customer, name='update_customer'),
    path('product/create/', create_product, name='create_product'),
    path('product/update/<int:product_id>/', update_product, name='update_product'),
    path('order/create/', create_order, name='create_order'),
    path('order/update/<int:order_id>/', update_order, name='update_order'),
    
]