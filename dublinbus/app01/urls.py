from django.conf.urls import url
from django.urls import path
from app01 import views

urlpatterns = [
<<<<<<< Updated upstream
    url('index/', views.index),
    url('', views.home),
=======
    path('index/', views.index),
    path('', views.home),
    path('leapcard/',views.leapcard),
    path('init',views.init),
>>>>>>> Stashed changes
]