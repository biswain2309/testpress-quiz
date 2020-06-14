from django.contrib import admin
from django.urls import path,include
from home import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('home/', views.home, name='home'),
    path('home/instr/genknow', views.instr, name='gen'),
    path('home/genknow', views.genknow, name='genknow'),
]
