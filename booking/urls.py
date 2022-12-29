from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.index, name='index.html'),
    path('about', views.about, name='about.html'),
    path('room/<int:pk>/', views.room, name='room.html'),
    path('room_detail/<int:pk>/', views.room_detail, name='room_detail.html'),
    path('price_filter', views.filter_by_prices, name='price_filter.html'),
    path('blog', views.read_feeds, name='blog.html'),
    path('contact', views.contact, name='contact.html'),
    path('subscribe', views.subscribe, name='subscribe.html'),
    path('register', views.register, name='register.html'),
    path('login', views.log_in, name='login.html'),
    path('logout', views.log_out, name='logout.html'),
    path('search_room', views.search_room, name='search_room.html'),
    path('subcategories', views.read_subcategories, name='subcategories.html'),
]
