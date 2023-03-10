from django.db import models

# Create your models here.

# from booking.models import Room, RoomSubCategory


class Order(models.Model):
    username = models.CharField(max_length=50, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    state = models.CharField(max_length=20,
        choices=[
            ('draft','Draft'),
            ('confirmed', 'Confirmed'),
            ('checked_in', 'Checked In'),
            ('checked_out', 'Checked Out'),
            ('done', 'Done'),
            ('cancel', 'Cancel')
        ])

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    room = models.ForeignKey(Room,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
