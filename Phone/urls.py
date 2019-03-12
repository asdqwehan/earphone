"""Phone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
from Phone.settings import MEDIA_ROOT
from Buyers import views

urlpatterns = [
    url(r'^media/(?P<path>.*)', serve, {"document_root":MEDIA_ROOT}), #MEDIA显示图片的URL
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^shops/', include('Shops.urls', namespace='Shops')),
    url(r'^buyers/', include('Buyers.urls', namespace='Buyers')),
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^products/(?P<products_id>\d+)/$', views.products, name='products'),
    url(r'^product_details/(?P<product_id>\d+)/$', views.product_details, name='product_details'),
    url(r'^register/$', views.register, name='register'),
    url(r'^sendmessage/$', views.sendMessage, name='sendmessage'),
]

'''
urlpatterns += [
    url(r'^products/(\d+)/$', views.products, name='products'),
]
'''
urlpatterns += [
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^addtobuycar/(?P<product_id>\d+)/$', views.addToBuycar, name='addtobuycar'),
    url(r'^cart/delete_car_goods/(?P<product_id>\d+)/$', views.delete_car_goods, name='delete_car_goods'),
    url(r'^enterorder/$', views.enterorder, name='enterorder'),
    url(r'^buyers/enterpay/$', views.enterpay, name='entrypay'),
    url(r'^buyers/payVerify/(?P<num>\d+)/$', views.payVerify),
]