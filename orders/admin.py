from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

def mark_paid(modeladmin, request, queryset):
    queryset.update(paid = True)
mark_paid.short_description = "Mark Selected Orders' Paid to True"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email',
                    'address', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    search_fields = ('address',)
    actions = [mark_paid]
