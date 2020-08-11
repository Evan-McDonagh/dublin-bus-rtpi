from django.conf.urls import url
from django.urls import path

from user_manage import views

app_name = 'user_manage'

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^addfav/', views.addfav, name='addfav'),
    url(r'^showuserinfowindow/', views.showuserinfowindow, name='showuserinfowindow'),
    url(r'^getfav/', views.getfav, name='getfav'),
    url(r'^delfav/', views.delfav, name='delfav'),
    url(r'^test/', views.test, name='test'),
    # url('', views.register)
    # path('register', views.register),
    # path('register_form', views.register_form, name = 'register_form'),
    # path('', views.register)
]
