from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Vendor, Customer, Category, Product, ProductImage, ProductAttribute, Order, OrderItem, Payment, Delivery, Review

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'password1', 'password2']
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Username'
    }))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Email Address'
    }))
    
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Phone Number'
    }))
    
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Address'
    }))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Password'
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Confirm Password'
    }))

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'phone', 'address']
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Username'
    }))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Email Address'
    }))
    
    role = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Role'
    }))
    
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Phone Number'
    }))
    
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Address'
    }))

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['store_name', 'business_details', 'location', 'logo_url', 'is_approved']
    
    store_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Store Name'
    }))
    
    business_details = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Business Details',
        'rows': 4
    }))
    
    location = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Location'
    }))
    
    logo_url = forms.URLField(widget=forms.URLInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Logo URL'
    }))
    
    is_approved = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'focus:ring-blue-500 text-blue-600'
    }))

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['shipping_address', 'billing_address']
    
    shipping_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Shipping Address'
    }))
    
    billing_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Billing Address'
    }))

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'parent_category']
    
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Category Name'
    }))
    
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Category Description',
        'rows': 4
    }))
    
    parent_category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500'
    }))

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['vendor', 'name', 'description', 'price', 'stock_quantity', 'sku', 'is_active', 'categories']
    
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Product Name'
    }))
    
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Product Description',
        'rows': 4
    }))
    
    price = forms.DecimalField(max_digits=9, decimal_places=2, widget=forms.NumberInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Price'
    }))
    
    stock_quantity = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Stock Quantity'
    }))
    
    sku = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'SKU'
    }))
    
    is_active = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'focus:ring-blue-500 text-blue-600'
    }))
    
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.SelectMultiple(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500'
    }))

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'total_amount', 'status']
    
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), widget=forms.Select(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500'
    }))
    
    total_amount = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Total Amount'
    }))
    
    status = forms.ChoiceField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], widget=forms.Select(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500'
    }))


    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'customer', 'comment','rating']
    
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500'
    }))
    
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), widget=forms.Select(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500'
    }))
    
    rating = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Rating (1-5)'
    }))
    
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'Your Comment',
        'rows': 4
    }))
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return rating
