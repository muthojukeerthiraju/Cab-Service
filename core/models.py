from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from PIL import Image

GENDER_CHOICES =(
    (1, "only male"),
    (2, "only female"),
    (0, "no specific choice")

)

# Create your models here.
def validate_luggage(value):
    if  (value<20):
        return value
    else:
        raise ValidationError("luggage is exceeded")


def validate_people(value):
    if  (value<4):
        return value
    else:
        raise ValidationError("persons are exceeded")


class Booking(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    created_by=models.CharField(max_length=50)
    pick_up_point=models.CharField(max_length=250)
    destination=models.CharField(max_length=250)
    booked = models.BooleanField(default=False)
    date=models.DateField()
    time=models.TimeField()
    window_for_pickup_time=models.DurationField()
    ammount_of_luggage=models.IntegerField(validators =[validate_luggage], default=0)
    number_of_people=models.IntegerField(validators =[validate_people], default=1)
    def get_absolute_url(self):
        return reverse('core:myBookings')
    def __str__(self):
        return self.pick_up_point+'-'+self.destination+'-'+str(self.booked)+'-'+str(self.id)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Message(models.Model):
     sender =  models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
     reciever = models.ForeignKey(User,on_delete=models.CASCADE, related_name="reciever")
     msg_content = models.CharField(max_length=10000)
    # created_at = models.CharField(max_length=1000)
     def __str__(self):
         return self.sender.username+'-'+self.reciever.username

     def save(self, *args, **kwargs):
         super().save(*args, **kwargs)




class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg',upload_to='profile_pics')
    def __str__(self):
        return self.user.username

    def save(self,**kwargs):
        super().save()
