from django.shortcuts import render,HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
import random, datetime, time, hashlib
from Buyers.models import *
from Phone.settings import EMAIL_HOST_USER
from django.core.urlresolvers import reverse

def index(request):
    return render(request, 'buyers/index.html', locals())

def login(request):
    return render(request, 'buyers/login.html', locals())

def cart(request):
    return render(request, 'buyers/cart.html', locals())

def products(request):
    return render(request, 'buyers/products.html', locals())

def product_details(request):
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