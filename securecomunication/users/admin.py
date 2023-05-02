from django.contrib import admin

# Register your models here.
from .models import Users,Customers

admin.site.register(Users)
admin.site.register(Customers)