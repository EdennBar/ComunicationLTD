from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_message = f"This is the token for the password reset: {reset_password_token.key}," \
                    f"Click here to change your password: https://localhost:3000/password-reset/{reset_password_token.key}"
    email_title = "Secure Comm LTD"
    send_mail(f'Password Reset for {email_title}', email_message, 'noreply@securecommltd',
              [reset_password_token.user.email])


class Users(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=250)
    # date_created = models.DateTimeField(blank=True, null=True)
    # is_superuser = None
    # is_staff = None
    is_superuser = models.BooleanField(default=False)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Customers(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=100, unique=True)
    REQUIRED_FIELDS = ['name', 'address', 'phone']

    class Meta:
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.name
