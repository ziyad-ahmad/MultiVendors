from django.shortcuts import render, redirect
from django.contrib.auth import login
from .Forms import UserRegistrationForm, UserUpdateForm, VendorForm
from .Forms import CustomerForm, ProductForm, OrderForm
from .models import User, Vendor, Customer, Product, Order, Category,Payment,OrderItem
from django.contrib.auth.decorators import user_passes_test, login_required

# Check if the user is an admin
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@user_passes_test(is_admin)
def admin_dashboard(request):
    vendors = Vendor.objects.all()
    products = Product.objects.all()
    orders = Order.objects.all()
    payments = Payment.objects.all()

    context = {
        'vendors': vendors,
        'products': products,
        'orders': orders,
        'payments': payments,
    }
    return render(request, 'admin/dashboard.html', context)

@user_passes_test(is_admin)
def approve_vendor(request, vendor_id):
    vendor = Vendor.objects.get(id=vendor_id)
    vendor.is_approved = True
    vendor.save()
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def approve_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.is_active = True
    product.save()
    return redirect('admin_dashboard')

@login_required
def vendor_dashboard(request):
    vendor = request.user.vendor
    products = Product.objects.filter(vendor=vendor)
    orders = Order.objects.filter(items__product__vendor=vendor).distinct()

    context = {
        'products': products,
        'orders': orders,
    }
    return render(request, 'vendor/dashboard.html', context)

@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to product list
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})

@login_required
def update_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product_id)  # Redirect to product detail
    else:
        form = ProductForm(instance=product)
    return render(request, 'update_product.html', {'form': form})



@login_required
def customer_dashboard(request):
    products = Product.objects.filter(is_active=True)
    orders = Order.objects.filter(customer=request.user.customer)

    context = {
        'products': products,
        'orders': orders,
    }
    return render(request, 'customer/dashboard.html', context)

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('customer_dashboard')

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    order = Order.objects.create(customer=request.user.customer, total_amount=cart.total_price())
    
    for item in cart.items.all():
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
    
    cart.items.all().delete()
    return redirect('order_detail', order_id=order.id)

def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:6]  # Show only 6 featured products
    categories = Category.objects.all()  
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'home.html', context)

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')  # Redirect to home page
    else:
        form = UserRegistrationForm()
    return render(request, 'register_user.html', {'form': form})

@login_required
def update_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', user_id=user_id)  # Redirect to user profile
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'update_user.html', {'form': form})

def create_vendor(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vendor_list')  # Redirect to vendor list
    else:
        form = VendorForm()
    return render(request, 'create_vendor.html', {'form': form})

def update_vendor(request, vendor_id):
    vendor = Vendor.objects.get(id=vendor_id)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('vendor_detail', vendor_id=vendor_id)  # Redirect to vendor detail
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'update_vendor.html', {'form': form})

def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')  # Redirect to customer list
    else:
        form = CustomerForm()
    return render(request, 'create_customer.html', {'form': form})

def update_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', customer_id=customer_id)  # Redirect to customer detail
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'update_customer.html', {'form': form})


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')  # Redirect to order list
    else:
        form = OrderForm()
    return render(request, 'create_order.html', {'form': form})

def update_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_detail', order_id=order_id)  # Redirect to order detail
    else:
        form = OrderForm(instance=order)
    return render(request, 'update_order.html', {'form': form})

