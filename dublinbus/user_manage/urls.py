from django.conf.urls import url
from django.urls import path

from user_manage import views

app_name = 'user_manage'

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    # url('', views.register)
    # path('register', views.register),
    # path('register_form', views.register_form, name = 'register_form'),
    # path('', views.register)
]
