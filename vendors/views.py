from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from .cart import Cart
from .Forms import UserRegistrationForm, UserUpdateForm, CustomerForm, ProductForm, OrderForm, VendorRegistrationForm, ProductImageForm
from .models import User, Vendor, VendorDocument, Customer, Product, Order, Category, Payment, OrderItem, Category, ProductImage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Helper function to check if the user is an admin
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

# Admin Dashboard
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
def vendor_registration(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        vendor_form = VendorRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid() and vendor_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'vendor'
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            vendor.save()
            for file in request.FILES.getlist('documents'):
                VendorDocument.objects.create(vendor=vendor, document=file)
            login(request, user)
            return redirect('vendor_dashboard')
    else:
        user_form = UserCreationForm()
        vendor_form = VendorRegistrationForm()
    return render(request, 'vendor_registration.html', {'user_form': user_form, 'vendor_form': vendor_form})

@user_passes_test(lambda u: u.is_superuser)
def admin_vendor_management(request):
    """
    View for managing vendors, including searching, pagination, document viewing, and approval/rejection.
    """
    # Fetch all vendors
    vendors = Vendor.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        vendors = vendors.filter(store_name__icontains=search_query) | vendors.filter(location__icontains=search_query)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(vendors, 10)  # Show 10 vendors per page
    try:
        vendors = paginator.page(page)
    except PageNotAnInteger:
        vendors = paginator.page(1)
    except EmptyPage:
        vendors = paginator.page(paginator.num_pages)

    # Handle viewing vendor documents
    vendor_id = request.GET.get('vendor_id')
    if vendor_id:
        vendor = get_object_or_404(Vendor, id=vendor_id)
        documents = VendorDocument.objects.filter(vendor=vendor)
        return render(request, 'admin/admin_vendor_management.html', {
            'vendors': vendors,  # Paginated vendor list
            'selected_vendor': vendor,  # Selected vendor for document viewing
            'documents': documents,  # Vendor documents
            'search_query': search_query,  # Current search query
        })

    # Handle approving or rejecting a vendor
    if request.method == 'POST':
        vendor_id = request.POST.get('vendor_id')
        vendor = get_object_or_404(Vendor, id=vendor_id)

        if 'approve_vendor' in request.POST:
            vendor.is_approved = True
            vendor.save()
            messages.success(request, f"{vendor.store_name} has been approved.")

            # Send email notification to the vendor
            send_mail(
                'Vendor Approval Notification',
                f'Congratulations! Your vendor account for {vendor.store_name} has been approved.',
                'admin@example.com',
                [vendor.user.email],
                fail_silently=False,
            )

        elif 'reject_vendor' in request.POST:
            rejection_reason = request.POST.get('rejection_reason')
            vendor.is_approved = False
            vendor.save()
            messages.success(request, f"{vendor.store_name} has been rejected. Reason: {rejection_reason}")

            # Send email notification to the vendor
            send_mail(
                'Vendor Rejection Notification',
                f'We regret to inform you that your vendor account for {vendor.store_name} has been rejected. Reason: {rejection_reason}',
                'admin@example.com',
                [vendor.user.email],
                fail_silently=False,
            )

        return redirect('admin_vendor_management')

    # Default: Display the list of all vendors
    return render(request, 'admin/admin_vendor_management.html', {
        'vendors': vendors,  # Paginated vendor list
        'search_query': search_query,  # Current search query
    })

# Vendor Dashboard
@login_required
def vendor_dashboard(request):
    if not hasattr(request.user, 'vendor'):
        raise PermissionDenied("You are not a vendor.")
    
    vendor = request.user.vendor
    products = Product.objects.filter(vendor=vendor)
    orders = Order.objects.filter(items__product__vendor=vendor).all()

    context = {
        'products': products,
        'orders': orders,
    }
    return render(request, 'vendor/dashboard.html', context)


# Add Product
def create_product(request):
    # Check if the user is a vendor
    if not hasattr(request.user, 'vendor'):
        raise PermissionDenied("You are not a vendor.")

    if request.method == 'POST':
        form = ProductForm(request.POST)
        img_form = ProductImageForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the product with the vendor association
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.save()

            # Handle product images
            if img_form.is_valid():
                for file in request.FILES.getlist('image'):
                    ProductImage.objects.create(product=product, image=file)
            
            return redirect('vendor_dashboard')
    else:
        form = ProductForm()
        img_form = ProductImageForm()

    return render(request, 'vendor/add_product.html', {'form': form, 'imgForm': img_form})

@login_required
def update_product(request, product_id):
    # Retrieve the product or return a 404 error
    product = get_object_or_404(Product, id=product_id)
    if product.vendor != request.user.vendor:
        raise PermissionDenied("You do not have permission to edit this product.")

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')
    else:
        form = ProductForm(instance=product)

    return render(request, 'update_product.html', {'form': form})


def genHome(request):
    
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:5].prefetch_related(
        'images'
    )
    
    high_rated_products = Product.objects.filter(is_active=True).order_by('-rating')[:5].prefetch_related(
        'images'
    )

    # Function to attach primary image URLs to products
    def attach_primary_image(products):
        for product in products:
            primary_image = next((img for img in product.images.all() if img.is_primary), None)
            product.primary_image = primary_image.image.url if primary_image else None

    # Attach primary images to both product lists
    attach_primary_image(latest_products)
    attach_primary_image(high_rated_products)

    context = {
        'latest_products': latest_products,
        'high_rated_products': high_rated_products,
    }
    
    return render(request, 'genHome.html', context)

def category_home(request, category_id=None):
    # Fetch all active categories
    categories = Category.objects.filter(is_active=True)
    
    if category_id:
        category = get_object_or_404(Category, id=category_id, is_active=True)
        products = Product.objects.filter(categories=category, is_active=True).select_related('vendor').prefetch_related('images', 'attributes')
    else:
        # If no category is selected, fetch all active products
        category = None
        products = Product.objects.filter(is_active=True).select_related('vendor').prefetch_related('images', 'attributes')
    
    context = {
        'categories': categories,
        'products': products,
        'category': category,  # Pass the selected category (if any)
    }
    return render(request, 'home.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_images = product.images.all()
    product_attributes = product.attributes.all()
    
    average_rating = product.rating

    related_products = Product.objects.filter(categories__in=product.categories.all(), is_active=True).exclude(id=product.id).distinct()[:5]
    
    for related_product in related_products:
        primary_image = related_product.images.filter(is_primary=True).first()
        related_product.primary_image = primary_image.image.url if primary_image else None

    context = {
        'product': product,
        'product_images': product_images,
        'product_attributes': product_attributes,
        'average_rating': average_rating,
        'related_products': related_products,
    }
    
    return render(request, 'product_detail.html', context)


# Customer Dashboard
@login_required
def customer_dashboard(request):
    if not hasattr(request.user, 'customer'):
        raise PermissionDenied("You are not a customer.")
    
    products = Product.objects.filter(is_active=True)
    orders = Order.objects.filter(customer=request.user.customer)

    context = {
        'products': products,
        'orders': orders,
    }
    return render(request, 'customer/dashboard.html', context)

# Add to Cart (Customer)
def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id=product_id, quantity=1)
    messages.success(request, 'Product added to cart!')
    return redirect('category_home')


def cart_view(request):
    cart = Cart(request)
    items = cart.get_items()
    subtotal = cart.get_total_price()
    shipping_estimate = subtotal * 0.02
    tax_estimate = subtotal * 0.1
    order_total = subtotal + shipping_estimate + tax_estimate

    context = {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
        'shipping_estimate': shipping_estimate,
        'tax_estimate': tax_estimate,
        'order_total': order_total,
    }
    return render(request, 'cart_vew.html', context)


def update_cart(request, product_id):
    cart = Cart(request)
    action = request.POST.get('action')
    current_quantity = cart.get_item_quantity(product_id)

    if action == 'increment':
        new_quantity = current_quantity + 1
    elif action == 'decrement':
        new_quantity = max(current_quantity - 1, 1)
    else:
        new_quantity = current_quantity

    cart.add(product_id=product_id, quantity=new_quantity, update_quantity=True)
    messages.success(request, 'Cart updated successfully!')
    return redirect('cart_view')


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id=product_id)
    messages.success(request, 'Product removed from cart.')
    return redirect('cart_view')


def checkout(request):
    cart = Cart(request)
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            total_price = sum(
                item['product'].initial_sell * int(item['quantity']) for item in cart.get_items()
            )
            order = form.save(commit=False)
            order.created_by = request.user
            order.paid_amount = total_price
            order.save()

            for item in cart.get_items():
                product = item['product']
                quantity = int(item['quantity'])
                price = product.initial_sell * quantity
                OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
            cart.clear()
            messages.success(request, "Your order has been placed successfully!")
            return redirect('myaccount')
        else:
            messages.error(request, "There was an issue with your order. Please try again.")

    return render(request, 'checkout.html', {'cart': cart, 'form': form})

# Home Page
def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:6]
    categories = Category.objects.all()
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'home.html', context)

# User Registration
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register_user.html', {'form': form})

# Update User Profile
@login_required
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user != user:
        raise PermissionDenied("You do not have permission to edit this profile.")
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', user_id=user_id)
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'update_user.html', {'form': form})

def create_vendor(request):
    """
    View for creating a new vendor.
    """
    if request.method == 'POST':
        # Bind the form to the POST data
        form = VendorRegistrationForm(request.POST)
        if form.is_valid():
            # Save the vendor and display a success message
            vendor = form.save()
            messages.success(request, f"Vendor '{vendor.store_name}' has been created successfully!")
            return redirect('vendor_list')  # Redirect to the vendor list page
        else:
            # Display an error message if the form is invalid
            messages.error(request, "Please correct the errors below.")
    else:
        # Display an empty form for GET requests
        form = VendorRegistrationForm()

    # Render the form in the template
    return render(request, 'create_vendor.html', {'form': form})

# Update Vendor
def update_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    if request.method == 'POST':
        form = vendor_registration(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('vendor_detail', vendor_id=vendor_id)
    else:
        form = vendor_registration(instance=vendor)
    return render(request, 'update_vendor.html', {'form': form})

# Create Customer
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'create_customer.html', {'form': form})

# Update Customer
def update_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', customer_id=customer_id)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'update_customer.html', {'form': form})

# Create Order
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'create_order.html', {'form': form})

# Update Order
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_detail', order_id=order_id)
    else:
        form = OrderForm(instance=order)
    return render(request, 'update_order.html', {'form': form})
