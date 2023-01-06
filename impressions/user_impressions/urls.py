from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('create/', CreateRememberView.as_view(), name="create_remember"),
    path('<str:slug>/', details, name="remember_detail"),
    path('<str:slug>/del/', remember_delete, name="remember_delete"),
]
