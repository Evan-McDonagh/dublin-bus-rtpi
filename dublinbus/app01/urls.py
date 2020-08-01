from django.conf.urls import url
from django.urls import path

from app01 import views

urlpatterns = [
    url('^$', views.index),
    url('stop/', views.stop),
    url('leapcard/',views.leapcard),
    # url('real_info/',views.real_info),
    url('init',views.init),
    url('weather',views.weather),
    url('printresult', views.printresult),
    url('rtmarkerinfo', views.rtmarkerinfo),
    url('showprediction', views.showprediction),
    url('routesearch', views.routesearch),
    url('errorhandler', views.errorhandler),
]