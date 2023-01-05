from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('start.urls'), name="login"),
    path('', include("social_django.urls"), name="social"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout")
]
