from django.conf.urls import url
from Buyers import views

urlpatterns = [
    url(r'^cart/$', views.cart, name='cart'),
]