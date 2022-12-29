from sunau import Au_read
from django.db import models
import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User

class RoomCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    average_area = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to="booking/images",
        default="booking/images/default.png")
    description = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta():
        ordering = ('-average_area',)

    def get_subcategories(self):
        subcategories = RoomSubCategory.objects.filter(category_id=self.id)
        return subcategories

    def get_rooms(self):
        rooms = []
        for subcategory in self.get_subcategories():
            for room in Room.objects.filter(subcategory_id=subcategory.id):
                rooms.append(room)
        return rooms

    def get_available_rooms(self, checkin_date, checkout_date):
        available_rooms = []
        for room in self.get_rooms():
            if room.check_available(checkin_date, checkout_date):
                available_rooms.append(room)
        return available_rooms

class RoomSubCategory(models.Model):
    category_id = models.ForeignKey(RoomCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, unique=True)
    default_area = models.FloatField()
    default_capacity = models.IntegerField()
    default_price = models.FloatField()
    image = models.ImageField(upload_to="booking/images",
        default="booking/images/default.png")
    description = RichTextUploadingField(blank=True, null=True)
    viewed = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Room(models.Model):
    subcategory_id = models.ForeignKey(RoomSubCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, unique=True)
    area = models.FloatField(default=0.0)
    capacity = models.IntegerField()
    floor = models.IntegerField()
    price = models.FloatField()
    image = models.ImageField(upload_to="booking/images",
        default="booking/images/default.png")
    description = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    def check_available(self, checkin_date, checkout_date):
        booking_requests = BookingRequest.objects.filter(
            checkin_date__range=[checkin_date, checkout_date],
            checkout_date__range=[checkin_date, checkout_date])
        ids_room = []
        for request in booking_requests:
            if request.state in ['confirmed', 'checked_in', 'checked_out']:
                booking_request_items = BookingRequestItem.objects.filter(
                    booking_request_id=request.id)
                for item in booking_request_items:
                    ids_room.append(item.room_id.id)
        if self.id in ids_room:
            return False
        return True

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10,
        choices=[
            ('male','Male'),
            ('female', 'Female')
        ])
    id_number = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name

class BookingRequest(models.Model):
    code = models.CharField(max_length=20)
    customer_id = models.ForeignKey(Customer, on_delete=models.PROTECT)
    booking_date = models.DateField()
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
    note = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return self.code

    def get_total(self):
        return sum(
            room.get_amount() for room in BookingRequestItem.items.all())

class BookingRequestItem(models.Model):
    booking_request_id = models.ForeignKey(
        BookingRequest, on_delete=models.PROTECT)
    room_id = models.ForeignKey(Room, on_delete=models.PROTECT)
    price = models.FloatField()
    count_guests = models.IntegerField()

    def get_amount(self):
        return self.price

class Contact(models.Model):    
    name = models.CharField(max_length=150)
    email = models.EmailField()  
    phone= models.CharField(max_length=20, null=True)
    subject = models.CharField(max_length=264)
    message = models.TextField()

    def __str__(self):
        return self.name + " - " + self.subject

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    phone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.user.username 
