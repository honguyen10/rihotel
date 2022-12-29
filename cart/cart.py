from decimal import Decimal
from django.conf import settings
from booking.models import RoomSubCategory


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        sucategory_ids = self.cart.keys()
        # get the product objects and add them to the cart
        subcategories = RoomSubCategory.objects.filter(id__in=sucategory_ids)

        cart = self.cart.copy()
        for subcategory in subcategories:
            cart[str(subcategory.id)]['subcategory'] = subcategory

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, subcategory, quantity):
        """
        Add a product to the cart.
        """
        subcategory_id = str(subcategory.id)
        # import pdb; pdb.set_trace()
        subcategory_data = self.cart.get(subcategory_id, {})
        subcategory_data.update({
            'quantity': quantity
        })


        if subcategory_id not in self.cart:
            self.cart[subcategory_id] = {'quantity': quantity,
                                      'price': subcategory.default_price}
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, subcategory):
        """
        Remove a product from the cart.
        """
        subcategory_id = str(subcategory.id)
        if subcategory_id in self.cart:
            del self.cart[subcategory_id]
            self.save()

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
