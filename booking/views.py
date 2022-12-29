from operator import sub
import re
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, F, Value
from RiHotel.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
import datetime
import feedparser
import json
import urllib.request

DEFAULT_ENCODING = 'utf-8'

# rest_framework
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import RoomSubCategorySerializer, RoomCategorySerializer

from cart.cart import Cart
from django.template.defaulttags import register





# Create your views here.

@register.filter
def get_item(dictionary, key):
    return dictionary and dictionary.get(key) or None

categories = models.RoomCategory.objects.order_by("-average_area")

def index(request):
    subcategory_list = models.RoomSubCategory.objects.all()
    username = request.session.get('username', 0)
    
    return render(request, 'booking/index.html',
                {
                    'subcategory_list': subcategory_list,
                    'categories': categories,
                    'username': username,
                })

def about(request):
    username = request.session.get('username', 0)
    return render(request, 'booking/about.html',
                {
                    'categories': categories,
                    'username': username,
                })

def room(request, pk):
    subcategory_list = []
    if pk != 0:
        subcategory_list = models.RoomSubCategory.objects.filter(
            category_id=pk)
    else:
        subcategory_list = models.RoomSubCategory.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(subcategory_list, 9)
    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        rooms = paginator.page(1)
    except EmptyPage:
        rooms = paginator.page(paginator.num_pages)
    
    username = request.session.get('username', 0)
    
    return render(request, 'booking/room.html',
                {
                    'subcategory_list': subcategory_list,
                    'categories': categories,
                    'rooms': rooms,
                    'pk': pk,
                    'username': username,
                })

def room_detail(request, pk):
    selected_room = models.RoomSubCategory.objects.get(pk=pk)
    models.RoomSubCategory.objects.filter(pk=selected_room.pk).update(viewed=F('viewed')+1)
    selected_room.refresh_from_db()

    subcategory_list = models.RoomSubCategory.objects.all()
    
    username = request.session.get('username', 0)

    return render(request, 'booking/room_detail.html',
                            {
                                'subcategory_list': subcategory_list,
                                'selected_room': selected_room,
                                'pk': pk,
                                'categories': categories,
                                'username': username,
                            })

def blog(request):
    username = request.session.get('username', 0)
    return render(request, 'booking/blog.html',
                {
                    'categories': categories,
                    'username': username,
                })

def contact(request):
    username = request.session.get('username', 0)
    return render(request, 'booking/contact.html',
                    {
                        'categories': categories,
                        'username': username,
                    })

def search_room(request):
    global checkin_date
    global checkout_date
    global category_id

    subcategory_list = []

    if request.method == 'GET':
        form = forms.SearchRoom(request.GET)
        if form.is_valid():
            checkin_date = form.cleaned_data.get('checkin_date')
            checkout_date = form.cleaned_data.get('checkout_date')
            category_id = form.cleaned_data.get('category_id')

            if category_id != 0:
                category = models.RoomCategory.objects.get(pk=category_id)
                for room in category.get_available_rooms(checkin_date, checkout_date):
                    if room.subcategory_id not in subcategory_list:
                        subcategory_list.append(room.subcategory_id)
            else:
                all_category = models.RoomCategory.objects.all()
                for category in all_category:
                    for room in category.get_available_rooms(checkin_date, checkout_date):
                        if room.subcategory_id not in subcategory_list:
                            subcategory_list.append(room.subcategory_id)
    total_room = {}
    for subcategory in subcategory_list:
        room_list = []
        for room in models.Room.objects.filter(subcategory_id=subcategory.id):
            room_list.append(room)
            total_room[subcategory.id] = len(room_list)
    
    username = request.session.get('username', 0)

    print(Cart(request).cart)
    return render(request, 'booking/search_room.html',
                {
                    'total_room': total_room,
                    'categories': categories,
                    'subcategory_list': subcategory_list,
                    'checkin_date': checkin_date,
                    'checkout_date': checkout_date,
                    'username': username,
                    'cart': Cart(request).cart,
                })

def filter_by_prices(request):
    username = request.session.get('username', 0)
    global category_id
    if request.method == 'GET':
        category_id = request.GET.get('category_id')
        a = float(request.GET.get('price_from'))
        b = float(request.GET.get('price_to'))
        price_from = a
        price_to = b
        if(a > b):
            price_from = b
            price_to = a

    if category_id != "0":
        subcategory_list = models.RoomSubCategory.objects.filter(category_id=category_id)
    else:
        subcategory_list = models.RoomSubCategory.objects.all()

    subcategory_list = [subcategory for subcategory in subcategory_list if subcategory.default_price >=
                    price_from and subcategory.default_price <= price_to]

    return render(request, "booking/room.html",
                    {
                    'categories': categories,
                    'category_id': category_id,
                    'subcategory_list': subcategory_list,
                    'username': username,
                    })

def contact(request):
    result = ''
    form = forms.FormContact()

    if request.method == 'POST':
        result='Form POST'
        form = forms.FormContact(request.POST, models.Contact)
        result='Form Contatct'
        if form.is_valid():
            request.POST._mutable = True
            post = form.save(commit=False)
            post.name = form.cleaned_data['name']
            post.phone = form.cleaned_data['phone']
            post.email = form.cleaned_data['email']
            post.password = form.cleaned_data['subject']
            post.password = form.cleaned_data['message']
            post.save()
            result = "Cảm ơn quý khách đã liên hệ. Chúng tôi sẽ phản hồi trong thời gian sớm nhất."
    else:
        form = forms.FormContact()

    username = request.session.get('username', 0)
    
    return render(request, "booking/contact.html",
                  {
                   'form': form,
                   'result': result,
                   'categories': categories,
                   'username': username,
                   })

def subscribe(request):
    username = request.session.get('username', 0)
    if request.method == 'POST':
        email_address = request.POST.get("email")
        subject = 'Lời chào từ Ri Hotel'
        message = 'Hy vọng các thông tin ở đây sẽ giúp quý khách có một kỳ nghỉ tuyệt vời.'
        recepient = str(email_address)

        html_content = '<h2 style="color:blue"><i>Kính chào quý khách,</i></h2>'\
            + '<p>Cảm ơn quý khách đã ghé thăm website của <strong>Ri Hotel</strong>.</p>' \
            + '<p>' + message + '</p>'

        msg = EmailMultiAlternatives(
            subject, message, 'Ri Hotel <betrueri1123@gmail.com', [recepient])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # send_mail(subject, message, EMAIL_HOST_USER,
        #           [recepient], fail_silently=False)

        result = "Email từ Ri Hotel đã được gửi đến hộp thư của quý khách. Xin cảm ơn."

        return render(request, 'booking/base.html', {
                                                     'result': result,
                                                     'categories': categories,
                                                     'username': username,
                                                     })
    
    return render(request, 'booking/base.html',{
                                                'categories': categories,
                                                'username': username,
                                                })

def read_feeds(request):
    news_feed = feedparser.parse("https://hellodulich.com/feed/")
    entry = news_feed.entries
    
    username = request.session.get('username', 0)
    
    return render(request, 'booking/blog.html', {
                                                'feeds': entry,
                                                'categories': categories,
                                                'username': username,
                                                })

def register(request):
    registered = False
    if request.method == "POST":
        form_user = forms.UserForm(data=request.POST)
        form_por = forms.UserProfileInfoForm(data=request.POST)
        if (form_user.is_valid() and form_por.is_valid() and form_user.cleaned_data['password'] == form_user.cleaned_data['confirm']):
            user = form_user.save()
            user.set_password(user.password)
            user.save()

            profile = form_por.save(commit=False)
            profile.user = user
            profile.save()
            registered = True

            # Gửi email 
            email_address = form_user.cleaned_data['email']        
            subject = 'Tài khoản của Quý khách tại Ri Hotel đã được tạo.'
            message = 'Hãy cùng khám phá và trải nghiệm việc đặt phòng tại Ri Hotel.<br/> Trân trọng.'
            recepient = str(email_address)

            html_content = '<h2 style="color:blue"><i>Kính chào '+ form_user.cleaned_data['username']+',</i></h2>'\
                        + '<p>Chào mừng quý khách đến với <strong>Ri Hotel</strong> website.</p>' \
                        + '<p>'+ message +'</p>'      
        
            msg = EmailMultiAlternatives(subject, message, 'Ri Hotel <betrueri123@gmail.com>', [recepient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        if form_user.cleaned_data['password'] != form_user.cleaned_data['confirm']:
            form_user.add_error(
                'confirm', 'Mật khẩu xác nhận không đúng.')
            print(form_user.errors, form_por.errors)
    else:
        form_user = forms.UserForm()
        form_por = forms.UserProfileInfoForm()

    username = request.session.get('username', 0)
    
    return render(request, 'booking/register.html',
                  {'categories': categories,
                   'form_user': form_user,
                   'form_por': form_por,
                   'registered': registered,
                   'username': username,
                   })

def log_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            result = "Kính chào " + username
            request.session['username'] = username
            username = request.session.get('username', 0)
            return render(request, "booking/login.html", {'login_result': result,
                                                        'username': username,
                                                        'categories': categories,
                                                        })
        else:
            print("Quý khách không thể đăng nhập.")
            print("Username: {} và mật khẩu: {}".format(username, password))
            login_result = "Username hoặc mật khẩu không chính xác!"
            return render(request, "booking/login.html", {'login_result': login_result,
                                                        'categories': categories,
                                                        })
    else:
        return render(request, "booking/login.html", {'categories': categories,})


@login_required
def log_out(request):
    logout(request)
    result = "Quý khách đã đăng xuất. Quý khách có thể đăng nhập trở lại"
    return render(request, "booking/login.html", {'logout_result': result,
                                                'categories': categories,
                                                })

class RoomSubCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed store (or edited)
    """
    queryset = models.RoomSubCategory.objects.all()
    serializer_class = RoomSubCategorySerializer
    # Cấp quyền cho người dùng
    # permission_classes = [permissions.IsAdminUser] # đọc/ ghi
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # chỉ đọc

def read_subcategories(request):
    url = 'http://127.0.0.1:8000/api/subcategories/'

    urlResponse = urllib.request.urlopen(url)
    if hasattr(urlResponse.headers, 'get_content_charset'):
        encoding = urlResponse.headers.get_content_charset(DEFAULT_ENCODING)
    else:
        encoding = urlResponse.headers.getparam('charset') or DEFAULT_ENCODING
    
    subcategory_list = json.loads(urlResponse.read().decode(encoding))
    subcategory_list = sorted(subcategory_list, key=lambda x: x['viewed'], reverse=True)

    username = request.session.get('username', 0)
    
    return render(request, "booking/subcategories.html",
                  {
                    'subcategory_list': subcategory_list,
                    'username': username,
                    'categories': categories,
                  })
