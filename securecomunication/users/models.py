from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
   first_name = models.CharField(max_length=30)
   last_name = models.CharField(max_length=30)
   email = models.EmailField(max_length=100, unique=True)
   password = models.CharField(max_length=250)
   #date_created = models.DateTimeField(blank=True, null=True) 
   #is_superuser = None
   #is_staff = None
   is_superuser = models.BooleanField(default=False)
   username = None 
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
   class Meta:
      verbose_name_plural='Users'
    
   def __str__(self):
      return self.first_name + ' ' + self.last_name
