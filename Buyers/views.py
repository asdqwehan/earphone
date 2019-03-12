from django.shortcuts import render,HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
import random, datetime, time, hashlib
from Buyers.models import *
from Phone.settings import EMAIL_HOST_USER
from django.core.urlresolvers import reverse
from Shops.models import *
from alipay import AliPay

#COOKIE验证装饰器
def cookieVerify(fun):
    def inner(request, *args, **kwargs):
        username = request.COOKIES.get('username')
        session = request.session.get('username') #获取session
        user = Buyer.objects.filter(username=username).first()
        if user and session == username: #校验session
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('login'))
    return inner

def paydata(order_num, count):
    alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA18hbICZP2+yW1qsEd/jLZWvJKYELMK1dEOaMScyX6UXlSL68VHJ1u9xFfEwn0J7MJ1a6XihzCTlnVncUOzGy86n8cy1+DDjae4te0annz0wXTuWbLeCbVy3tXGn+yglosa2i0HKRBVGZzKjAqLgqluJTYNel144xYyqsnol70S6Wx5x6RueuNz3q9SoSS0zuckmLSnhUYqzzZqBm53+ekqXxX/Ayz7mm9j/rTReJRXTb3G/qivpP2TYdHd1dWE8WZW4gARLERs8sFVaKPkWkwFv5txVACKpHE0hjjLldnM7iFZGamD169+ns5XcKHQDIv2GgHfHqxlBACJ1jRI3NhQIDAQAB
    -----END PUBLIC KEY-----'''
    app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
    MIIEpAIBAAKCAQEA18hbICZP2+yW1qsEd/jLZWvJKYELMK1dEOaMScyX6UXlSL68VHJ1u9xFfEwn0J7MJ1a6XihzCTlnVncUOzGy86n8cy1+DDjae4te0annz0wXTuWbLeCbVy3tXGn+yglosa2i0HKRBVGZzKjAqLgqluJTYNel144xYyqsnol70S6Wx5x6RueuNz3q9SoSS0zuckmLSnhUYqzzZqBm53+ekqXxX/Ayz7mm9j/rTReJRXTb3G/qivpP2TYdHd1dWE8WZW4gARLERs8sFVaKPkWkwFv5txVACKpHE0hjjLldnM7iFZGamD169+ns5XcKHQDIv2GgHfHqxlBACJ1jRI3NhQIDAQABAoIBAEJU0r5VSKNAXTXsKFmA33Vz5sidZIU4Ja22UVW2UNRiqhLsnxQOg2aWVb3Z4ztcNUG6hVvAb2xcewm3XT69Dlec33/AckjriS4FL8afxiSRLXERX9yAeQAZnCeWZb5Rmh9UUwJk1XOfG/ovvdmfk2gCdsMER3S1vzTOv3WUqb0pVn7X9GbFXGmdMmoowfSdgCvAKePQq1Mx2EdmD/5U3WGAD7481cWlcqOjCGCLTydMSrF1+HpYGkA8bDXtST2AgAGOXUSPvVlN8VkwUXFNeiahDtAbVs/D5MXvwXY0WKfCNZGSNYO6zXVmQuCl61WwkjsWcpaj24rIUdCWHzB8o0ECgYEA9vzXZD0k+zmI4yyN5TIFi4vrP50kd4Cdmc/6WZwpPdtAiEFgiroN4B0kwXeS9S8qRFouQem3nEYTcwAU67d+6/ey65iuUHlv/cllCD+9fbwkrzlyTyp1x88bd9AS7Vs9kh/aQsYSqLYDMTxxpgdidGtKdG8RvClg8LJgSb9d0G0CgYEA36gFxohNXvVZysWLoUA4gkVWhfpnD8o7Utz911wZnY3TPHZcXrt8JXpQdRd48UY0Z7UTtcpmMqsROXmWIj+urPtpiZxaKR8Jmh2q+X95I6+SBxopjLiOqS1LtJaH56BnSQzFGpkomFxV/n0ewTvETLVeVdT3Yhg44JGvFiHlMnkCgYEArGIKPzcB0an1ZYEaRCZmgmAUwCCAbDvDQ7BJ7jM1Aaw+XRssM4bp2krc9X7sfd3+ZRiAApcKBLNQLcqXz3ERz8XhBdhZiWdIh9wBfQFn0xL2k6nHo4NiEyP06um53Bn7XjqHDmXKbiAjGEE0nQm4aMLdg2hl+2rx8uy8kZxT8P0CgYEAiXSkiA3BL3kvBFZAqIvlrvqaYKEyshuiNh0nzTIHdDNz/Zbo0jf75rSzuiMA65gwIQTC5llMUhuc7Gvzf30QB7REepSjPN6cciGFsO1NMEd5QfAsVRYgZ401F/nj8NE+aUD16pDyyCEHoO6Y9j2bOWHGZo4KtDkay7n9l2ahjFECgYA3SE+ONcOrTXxfPii2LV/CMUxnZDu0OOo0QBzv1DvZG+y4JeORKeo1jcC8nMX1Rvrx8mRhTYW7MTb75+RYsLn6lSU1TjCKIqBfzTC1WladPZcFoEEUsDdb65Rv7O747qjLMolg0TEtLMDtaTUPC/GuZCFRKt5aS60Kx0IpASHmcQ==
    -----END RSA PRIVATE KEY-----'''
    alipay = AliPay(
        appid = "2016092800614418", #支付宝app的ID
        app_notify_url = None, #回调函数
        app_private_key_string = app_private_key_string, #私钥字符
        alipay_public_key_string = alipay_public_key_string, #公钥字符
        sign_type = "RSA2", #加密方法
    )

    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no = str(order_num),
        total_amount = str(count), #将decimal类型转换为字符串交给支付宝
        subject = '数码家电',
        return_url = None,
        notify_url = None #可选，不填则使用默认notify url
    )
    return "https://openapi.alipaydev.com/gateway.do?" + order_string

def payVerify(request,num):
    order = Order.objects.get(id=int(num))
    order_num = order.order_number
    order_count = order.total
    url = paydata(order_num,order_count)
    return HttpResponseRedirect(url)

def index(request):
    return render(request, 'buyers/index.html', locals())

def login(request):
    result = {"statue": "error", "data": ""}
    if request.method == "POST" and request.POST:
        email = request.POST.get('email')
        user = Buyer.objects.filter(email=email).first()
        if user:
            pwd = lockpw(request.POST.get('password'))
            if pwd == user.password:              
                response = HttpResponseRedirect(reverse('index'))
                response.set_cookie('user_id', user.id, max_age=3600) #下发cookie
                response.set_cookie('username', user.username, max_age=3600) #下发cookie
                request.session['username'] = user.username #上传session
                return response
            else:             
                result['data'] = '密码错误'
        else:
            result['data'] = '用户名不存在'
    return render(request, 'buyers/login.html', locals())

def logout(request):
    response = HttpResponseRedirect(reverse('index'))
    response.delete_cookie('user_id') #删除cookie
    response.delete_cookie('username')
    del request.session['username'] #删除session
    return response

@cookieVerify
def cart(request):
    user_id= request.COOKIES.get('user_id')
    buycarGoods = BuyCar.objects.filter(user_id=user_id)
    alltotal = 0
    #data = {}
    for i in buycarGoods:
        #goods = Goods.objects.get(id=i.id)
        total = i.goods_num * i.goods_price
        alltotal += total
        #data.append({'total': total, 'goods': goods, 'js': goods.goods_id})
        #data['total'] = total
        #data['goods'] = goods
        #data['js'] = goods.goods_id
    context = {'total': total, 'alltotal': alltotal, 'buycarGoods': buycarGoods}
    return render(request, 'buyers/cart.html', context)

def delete_car_goods(request, product_id):
    userId = request.COOKIES.get('user_id')
    goods = BuyCar.objects.filter(user=int(userId), id=int(product_id))
    goods.delete()
    return HttpResponseRedirect(reverse('cart'))

def enterorder(request):
    alltotal = 0
    data = []
    userId = request.COOKIES.get('user_id')
    if request.method == 'POST' and request.POST:
        countLIST = request.POST.getlist('quantity')
        for i in range(0, len(countLIST)):
            buycar = BuyCar.objects.filter(user=userId)[i]
            buycar.goods_num = countLIST[i]
            buycar.save()
            total = int(buycar.goods_price) * int(buycar.goods_num)
            data.append({'total': total, 'goods': buycar})
            alltotal += total
    return render(request, 'buyers/enterorder.html', locals())

def enterpay(request):
    if request.POST and request.method == 'POST':
        alltotal = 0 
        goods_list = []
        userId = request.COOKIES.get('user_id')
        print(userId, type(userId))
        #取出购物车中用户确定要购买的商品
        buycar = BuyCar.objects.filter(user=userId)
        print(buycar, type(buycar))
        for goods in buycar:
            total = int(goods.goods_price) * int(goods.goods_num)
            goods_list.append({'total': total, 'goods': goods})
            alltotal += total

        #把地址存入地址表
        address = Address()
        address.address = request.POST.get('address')
        address.username = request.POST.get('name')
        address.phone = request.POST.get('phone')
        address.buyer = Buyer.objects.get(id=userId)
        address.save()

        #在订单表中生成订单
        order = Order()
        #订单编号 日期(年月日时分秒) + 随机 + 用户id
        now = datetime.datetime.now()
        order.order_number = now.strftime("%Y%m%d%H%M%S") + str(random.randint(10000, 99999)) + userId
        #状态 未支付 1 支付成功 2 配送中 3 交易完成 4 已取消 0
        order.order_time = now
        order.order_statue = 1
        order.total = alltotal 
        order.user = Buyer.objects.get(id=userId)
        order.order_address = address
        order.save()

        #订单商品
        for good in goods_list: #循环保存订单中的商品
            g = good["goods"]
            g_o = OrderGoods()
            g_o.good_id = g.id
            g_o.good_name = g.goods_name
            g_o.good_price = g.goods_price
            g_o.good_num = g.goods_num
            g_o.good_picture = g.goods_picture
            g_o.order = order
            g_o.save()
    return render(request, 'buyers/enterpay.html', locals())

def addToBuycar(request, product_id):
    result = {"status": "error", "data": ""}
    if request.method == 'GET':
        goods = Goods.objects.get(id=product_id)
        buycar = BuyCar()
        buycar.goods_id = goods.goods_id
        buycar.goods_name = goods.goods_name
        buycar.goods_price = goods.goods_price
        img = goods.image_set.all()[0]
        buycar.goods_picture = img.img_path
        buycar.goods_num = 1
        username = request.session['username']
        user = Buyer.objects.get(username=username)
        buycar.user = user
        buycar.save()
        result['status'] = 'success'
        result['data'] = '已添加'
    result['data'] = '添加失败'
    return JsonResponse(result)


def products(request, products_id):
    if products_id == 0:
        type = {'label': '全部耳机', 'descrption': '所有商品，尽情挑选，应有尽有'}
        goods = Goods.objects.all()
    else:
        type = Types.objects.get(id=products_id)
        goods = Goods.objects.filter(types=type)
    data = []
    for i in goods:
        img = i.image_set.first().img_path #取出商品的第一张图片路径
        data.append({'img': img, 'goods': i}) #将每个商品图片和信息的字典写到data列表中

    return render(request, 'buyers/products.html', {'type': type, 'data': data})

def product_details(request, product_id):
    goods = Goods.objects.get(id=product_id)
    imgs = goods.image_set.all()
    showGoods = Goods.objects.all().order_by('-goods_now_price')[0:3]
    data = []
    for i in showGoods:
        img = i.image_set.first().img_path #取出商品的第一张图片路径
        data.append({'img': img, 'goods': i})
    return render(request, 'buyers/product_details.html', locals())

def register(request):
    result = {"status": "error", "data": ""}
    if request.method == 'POST' and request.POST:
        email = request.POST.get('email')
        username = request.POST.get('username')
        message = request.POST.get('message')
        pwd = request.POST.get('password')
        db_email = EmailValid.objects.filter(email_address=email).first()
        if db_email:
            if message == db_email.value:
                now = time.mktime(
                    datetime.datetime.now().timetuple()
                )
                db_now = time.mktime(db_email.times.timetuple())
                if now - db_now > 86400:
                    result["status"] = "验证码已过期"
                    db_email.delete()
                else:
                    b = Buyer()
                    b.username = username
                    b.email = email
                    b.password = lockpw(pwd)
                    b.save()
                    db_email.delete()
                    return HttpResponseRedirect(reverse('login'))
            else:
                result["status"] = "验证码错误"
        else:
            result["status"] = "邮箱不匹配"
    return render(request, 'buyers/register.html', locals())

def lockpw(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    result = md5.hexdigest()
    return result

def getRandomData():
    result = str(random.randint(1000, 9999))
    return result

def sendMessage(request):
    result = {"status": "error", "data": ""}
    if request.method == 'GET':
        receiver = request.GET.get('email')
        try:
            subject = '耳机商城的邮件'
            text_content = ''
            value = getRandomData()
            html_content = """
                <div>
                    <p>您的验证码是：%s，请勿告诉他人。</p>
                </div>
                """%value
            message = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [receiver])
            message.attach_alternative(html_content, 'text/html')
            message.send()
        except Exception as e:
            result["data"] = str(e)
        else:
            result["status"] = "success"
            result["data"] = "验证码已发送"
            e= EmailValid()
            e.email_address = receiver
            e.value = value
            e.times = datetime.datetime.now()
            e.save()
        finally:
            return JsonResponse(result)