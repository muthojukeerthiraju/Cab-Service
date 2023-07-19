from django.contrib import admin

# Register your models here.

from core.models import Booking,Profile,Message
# Register your models to admin site, then you can add, edit, delete and search your models in Django admin site.


admin.site.register(Booking)


admin.site.register(Profile)


admin.site.register(Message)
