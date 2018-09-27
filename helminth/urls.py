from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.basic, name = 'basic')
    ]
