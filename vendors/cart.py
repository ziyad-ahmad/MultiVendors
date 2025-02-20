from django.conf import settings
from .models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            def __init__(self, request):
             
                self.session = request.session
                cart = self.session.get(settings.CART_SESSION_ID)
                if not cart:
                    # Initialize the cart in the session if it doesn't exist
                    cart = self.session[settings.CART_SESSION_ID] = {}
                self.cart = cart
            # Initialize the cart in the session if it doesn't exist
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and fetch the associated products from the database.
        """
        product_ids = self.cart.keys()

        # Get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        # Yield each cart item with additional total price calculation
        for item in self.cart.values():
            item['total_price'] = item['product'].price * item['quantity']
            yield item

    def __len__(self):
        """
        Count all the items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        """
        Save the cart session and mark it as modified.
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True


    def add(self, product_id, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id_str = str(product_id)
        if product_id_str not in self.cart:
            self.cart[product_id_str] = {'quantity': 0, 'initial_sell': 0.0}  # Initialize with default values

        if update_quantity:
            self.cart[product_id_str]['quantity'] = quantity  # Update quantity directly
        else:
            self.cart[product_id_str]['quantity'] += quantity  # Increment the quantity

        self.save()
        # self.session.modified = True
    def remove(self, product_id):
        """
        Remove a product from the cart by its ID.
        """
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_items(self):
        items = []
        for product_id, item in self.cart.items():
            try:
                product = Product.objects.get(id=product_id)
                items.append({
                    'product': product,
                    'quantity': item['quantity'],
                    'initial_sell': product.initial_sell,  # Using the model attribute directly
                })
            except Product.DoesNotExist:
                # Handle the case where the product no longer exists
                continue  # Or log the error

        return items

    def clear(self):
        """
        Remove all items from the cart.
        """
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
    def get_item_quantity(self, product_id):
      
        # Convert product_id to a string because keys in the session are stored as strings
        product_id_str = str(product_id)
        item = self.cart.get(product_id_str)
        if item:
            return item.get('quantity', 0)  # Return the quantity if it exists
        return 0
    def get_total_price(self):
        """
        Calculate the total price of all items in the cart.
        """
        total_price = 0
        for item in self.get_items():  # Get all items first
            total_price += item['initial_sell'] * item['quantity']  
        return total_price

