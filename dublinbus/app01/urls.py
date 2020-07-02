from django.conf.urls import url
from django.urls import path

from app01 import views

urlpatterns = [
    path('', views.base),
    path('search', views.search),
    path('stop', views.stop),
    path('leapcard',views.leapcard),
    path('init',views.init),
    path('weather',views.weather),
]