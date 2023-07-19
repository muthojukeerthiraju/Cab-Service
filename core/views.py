from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .forms import SignUpForm
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .forms import BookingForm,UserUpdateForm,ProfileUpdateForm,messageForm
from .models import Booking,Message
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('core:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'core/change_password.html', {
        'form': form
    })



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('core:login'))
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

def profile(request):
    if request.method == 'POST':
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account has been updated!')
            return redirect('core:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'core/profile.html',context)

def Bookingview(request):

    if  request.method == 'POST':
        form=BookingForm(request.POST)


        if form.is_valid():
            instance=form.save(commit=False)
            instance.user=request.user
            instance.save()
            print(form.errors)
            messages.success(request,f'Your Booking has been saved!')
            return redirect('core:myBookings')
        else:
            print("Form is invalid")
    else:
        form=BookingForm()


    return render(request,'core/Booking.html',{'form':form})



def messageview(request,user2id):

    if  request.method == 'POST':
        form=messageForm(request.POST)


        if form.is_valid():
            instance=form.save(commit=False)
            instance.sender=request.user
            instance.reciever=User.objects.get(id=user2id)
            instance.save()
            print(form.errors)
            messages.success(request,f'Your message has sent')
            return redirect('core:myBookings')
        else:
            print("Form is invalid")
    else:
        form=messageForm()


    return render(request,'core/message.html',{'form':form})






class AllBookingsListView(ListView):
    model = Booking
    queryset = Booking.objects.all()
    template_name = 'core/allBookings_lv.html'

    #def get_queryset(self):
    #    return Booking.objects.filter(destination=self.request.user)

class changeBooking(UpdateView):
    model = Booking
    fields = ['pick_up_point','destination','booked']
    template_name = 'core/Booking.html'


def MyBookingsListView(request):
    a=Booking.objects.filter(user=request.user)
    b=Booking.objects.all()
    object_list=[]
    if (b and a):
        for c in b:
            if((not c.booked) and c.user==a[0].user ):
                object_list.append(c)
    return render(request,'core/myBookings_lv.html',{'object_list':object_list})

def MydoneBookingsListView(request):
    a=Booking.objects.filter(user=request.user)
    b=Booking.objects.all()
    object_list=[]
    if (b and a):
        for c in b:
            if((c.booked) and c.user==a[0].user ):
                object_list.append(c)
    return render(request,'core/mydoneBookings_lv.html',{'object_list':object_list})

def detail(request,Booking_id):
    a=Booking.objects.filter(id=Booking_id)
    b=Booking.objects.all()
    object_list=[]
    for c in b:
        if((not c.booked)and c.destination==a[0].destination and c.user!=a[0].user and c.pick_up_point==a[0].pick_up_point):
            object_list.append(c)
    return render(request,'core/suggestions_lv.html',{'object_list':object_list})


def booked(request,Booking_id):
    a=Booking.objects.get(id=Booking_id)
    a.booked=True
    a.save()
    return redirect('core:myBookings')


def inbox(request):
    a=Message.objects.filter(reciever=request.user)
    b=Message.objects.all().order_by('-id')
    object_list=[]
    if (b and a):
        for c in b:
            if(c.reciever==a[0].reciever ):
                object_list.append(c)
    return render(request,'core/inbox_lv.html',{'object_list':object_list})


def outbox(request):
    a=Message.objects.filter(sender=request.user)
    b=Message.objects.all().order_by('-id')
    object_list=[]
    if (b and a):
        for c in b:
            if(c.sender==a[0].sender ):
                object_list.append(c)
    return render(request,'core/outbox_lv.html',{'object_list':object_list})


def unbooked(request,Booking_id):
    a=Booking.objects.get(pk=Booking_id)
    a.booked=False
    a.save()
    return redirect('core:myBookings')

def deleteBooking(request,Booking_id):
    a=Booking.objects.get(pk=Booking_id)
    a.delete()
    return redirect('core:myBookings')
