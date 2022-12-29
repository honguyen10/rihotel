from django.contrib import admin
from django.db.models import F
from .models import Contact, Customer, RoomCategory, RoomSubCategory, Room, BookingRequest, BookingRequestItem, UserProfileInfo
import datetime


admin.site.site_header = "Ri Hotel Admin"


def increase_viewed(modeladmin, request, queryset):
    queryset.update(viewed=F('viewed') + 1)
increase_viewed.short_description = "Increase Viewed by one unit"

class RoomSubCategoryA(admin.ModelAdmin):
    list_display = ('name', 'default_capacity', 'default_price', 'viewed')
    list_filter = ('category_id', 'default_capacity')
    search_fields = ("name__contains",)
    actions = [increase_viewed]

class RoomA(admin.ModelAdmin):
    list_display = ('name', 'area', 'capacity', 'floor', 'price')
    list_filter = ('subcategory_id', 'floor')
    search_fields = ("name__contains",)


admin.site.register(RoomCategory)
admin.site.register(RoomSubCategory, RoomSubCategoryA)
admin.site.register(Room, RoomA)
admin.site.register(Customer)
admin.site.register(BookingRequest)
admin.site.register(BookingRequestItem)
admin.site.register(Contact)
admin.site.register(UserProfileInfo)
