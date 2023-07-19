from django.contrib import admin
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path
from django.conf.urls import url, include
from . import views

app_name='core'

urlpatterns = [

    path('signup/', views.signup, name='signup'),
    path('login/',  LoginView.as_view(template_name='core/login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name= 'core/logged_out.html'),{'next_page': '/'}, name='logout'),
    path('Booking/', views.Bookingview, name='Booking'),
    path('message/<int:user2id>/', views.messageview, name='message'),
    path('profile/', views.profile, name='profile'),
    path('allBookings/',views.AllBookingsListView.as_view(),name='allBookings'),
    path('myBookings/',views.MyBookingsListView,name='myBookings'),
    path('mydoneBookings/',views.MydoneBookingsListView,name='mydoneBookings'),
    path('mydoneBookings/unbooked/<int:Booking_id>/',views.unbooked,name='unbooked'),
    path('myBookings/Bookingsuggestions/<int:Booking_id>/',views.detail,name='Bookingsuggestions'),
    path('myBookings/booked/<int:Booking_id>/',views.booked,name='booked'),
    path('myBookings/delete/<int:Booking_id>/',views.deleteBooking,name='myBookingsdelete'),
    path('mydoneBookings/delete/<int:Booking_id>/',views.deleteBooking,name='mydoneBookingsdelete'),
    path('myBookings/changeBooking/<pk>/',views.changeBooking.as_view(),name='changeBooking'),
    path('profile/changepassword/',views.change_password, name='change_password'),

    path('inbox/',views.inbox,name='inbox'),
    path('outbox/',views.outbox,name='outbox'),
]
