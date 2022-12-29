from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from booking.models import RoomCategory, RoomSubCategory, RoomCategory
from .cart import Cart
from .forms import CartAddProductForm

categories = RoomCategory.objects.all()

@require_POST
def cart_add(request, subcategory_id):
    cart = Cart(request)
    subcategory = get_object_or_404(RoomSubCategory, id=subcategory_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(subcategory=subcategory,
                 quantity=cd['room_quantity'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, subcategory_id):
    cart = Cart(request)
    subcategory = get_object_or_404(RoomSubCategory, id=subcategory_id)
    cart.remove(subcategory)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    username = request.session.get('username', 0)                                                               
    return render(request, 'cart/detail.html', {'cart': cart, 
                                                'username': username,
                                                'categories': categories})
