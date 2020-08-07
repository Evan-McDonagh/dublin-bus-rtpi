from django.conf.urls import url
from django.urls import path

from app01 import views

app_name = 'app01'

urlpatterns = [
    url('^$', views.index),
    url(r'^index$', views.index, name='index'),
    url(r'stop/', views.stop),
    url(r'leapcard/',views.leapcard),
    # url('real_info/',views.real_info),
    url(r'init/',views.init),
    url(r'weather/',views.weather),
    url(r'printresult/', views.printresult),
    url(r'rtmarkerinfo/', views.rtmarkerinfo),
    url(r'showprediction/', views.showprediction),
    url(r'routesearch/', views.routesearch),
    url(r'errorhandler/', views.errorhandler),
]