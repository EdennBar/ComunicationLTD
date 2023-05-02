"""
URL configuration for securecomunication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import index, register, login, password_change, add_customer, customers_list

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('admin/', admin.site.urls),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('password_change/', password_change, name='password_change'),
    path('customers/', add_customer, name='customers'),
    path('customers_list', customers_list, name='customers_list')

]
