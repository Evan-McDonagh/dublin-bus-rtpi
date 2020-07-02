from django.conf.urls import url
from django.urls import path

from app01 import views

urlpatterns = [
    # url('index/', views.index),
    path('^$', views.index),
    path('stop/', views.stop),
    path('leapcard/',views.leapcard),
    path('real_info/',views.real_info),
    path('twitter/',views.twitter),
]