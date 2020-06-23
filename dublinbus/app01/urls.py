from django.conf.urls import url

from app01 import views

urlpatterns = [
    url('index/', views.index),
    url('', views.home),
    url('leapcard/',views.leapcard),
    url('/init',views.init),
]