from django.db import models

class Buyer(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=32)

class Address(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    buyer = models.ForeignKey(Buyer)

class EmailValid(models.Model):
    value = models.CharField(max_length=32) #验证码
    email_address = models.EmailField() #邮箱
    times = models.DateTimeField() #注册时间，用于验证验证码是否过期

class BuyCar(models.Model):
    goods_id = models.CharField(max_length=32)
    goods_name = models.CharField(max_length=32)
    goods_price = models.FloatField()
    goods_picture = models.ImageField(upload_to="image")
    goods_num = models.IntegerField()
    user = models.ForeignKey(Buyer, on_delete=True)

#订单页面
class Order(models.Model):
    order_number = models.CharField(max_length=32) #订单编号
    order_time = models.DateTimeField(auto_now=True) #订单时间
    order_statue = models.CharField(max_length=32) #订单状态
    total = models.FloatField() #总计
    user = models.ForeignKey(Buyer, on_delete=True)
    order_address = models.ForeignKey(Address, on_delete=True)

#订单商品
class OrderGoods(models.Model):
    good_id = models.IntegerField()
    good_name = models.CharField(max_length=32)
    good_price = models.FloatField()
    good_num = models.IntegerField()
    goods_picture = models.ImageField()
    order = models.ForeignKey(Order, on_delete=True) #所属订单