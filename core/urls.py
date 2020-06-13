from django.urls import path,include
from . import views
from django.contrib.auth.views import PasswordResetView


urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]