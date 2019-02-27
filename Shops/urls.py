from django.conf.urls import url
from . import views
#from django.views.static import serve
#from Phone.settings import MEDIA_ROOT

urlpatterns = [
    url('^$', views.index, name='index'),
    #url(r'^static/(?P<path>.*)', django.views.static.serve, ('document_root': 'E:/Phone/Phone/static')),
    #url(r'^media/(?P<path>.*)', serve, {"document_root":MEDIA_ROOT}),
    url('^login/', views.login, name='login'),
    url('^goodsAdd/', views.goodsAdd, name='goodsadd'),
    url('^goodsList/', views.goodsList, name='goodslist'),
    url('^logout/', views.logout, name='logout'),
    url('^goodstypeadd/', views.goodsTypeAdd, name='goodstypeadd'),
    url(r'^goodschange/(?P<goods_id>\d+)/$', views.goodsChange, name='goodschange'),
    url(r'^goodsdel/(?P<goods_id>\d+)/$', views.goodsDel, name="goodsdel"),
    url(r'^goodsdetails/(?P<goods_id>\d+)/$', views.goodsDetails, name='goodsdetails'),

]