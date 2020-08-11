from django.conf.urls import url
from django.urls import path

from app01 import views

# app_name = "app01"
urlpatterns = [
    url('^$', views.index),
    url(r'^index', views.index),
    url('stop/', views.stop, name="stop"),
    url('leapcard/',views.leapcard, name="leapcard"),
    # url('real_info/',views.real_info),
    url('init',views.init, name="init"),
    url('weather',views.weather, name="weather"),
    url('printresult', views.printresult),
    url('rtmarkerinfo', views.rtmarkerinfo),
    url('showprediction', views.showprediction),
    url('routesearch', views.routesearch),
    url('errorhandler', views.errorhandler),
    
]