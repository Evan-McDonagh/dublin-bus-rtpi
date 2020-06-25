from django.conf.urls import url

from app01 import views

urlpatterns = [
    # url('index/', views.index),
    url('^$', views.index),
    url('stop/', views.stop),
    url('leapcard/',views.leapcard),
]