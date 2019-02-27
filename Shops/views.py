from django.shortcuts import render,HttpResponseRedirect
import hashlib, os
from Shops.models import *
from django.core.urlresolvers import reverse
from Phone.settings import MEDIA_ROOT
#cookie装饰器
def cookieVerify(fun):
    def inner(request, *args, **kwargs):
        username = request.COOKIES.get('username') #获取cookie中的username
        session = request.session.get('nickname') #获取session中的nickname
        db_user = Seller.objects.filter(username=username).first()
        if db_user and db_user.nickname == session: #校验session和cookies
            return fun(request, *args, **kwargs) #通过按照原函数返回
        else:
            return HttpResponseRedirect(reverse('Shops:login'))
    return inner

@cookieVerify
def index(request):
    return render(request, 'shops/index.html', locals())

def login(request):
    result = {'status':'errot', 'data':''} #状态标记，用来返回给前端页面登录不成功的原因
    if request.method == 'POST' and request.POST: #如果请求方式为POST并且有请求内容
        username = request.POST.get('username') #username是前台页面input标签中name属性所写内容
        #使用filter方法取出数据库中字段与前台输入相符的人
        db_user = Seller.objects.filter(username=username).first()
        if db_user:
            db_password = lockpw(db_user.password) #取该用户在数据库中的密码并加密
            password = lockpw(request.POST.get('password')) #取该用户在前台输入的密码并加密
            #password = request.POST.get('password')
            if db_password == password:
                #这里要给返回值设置cookie和session，所以要把返回值先赋值
                response = HttpResponseRedirect(reverse('Shops:index')) #登陆成功跳转至首页
                response.set_cookie('username', db_user.username, max_age=3600) #设置寿命为1小时的cookie
                request.session['nickname'] = db_user.nickname #设置session
                return response
            else:
                result['data'] = '密码错误'
        else:
            result['data'] = '用户名不存在'
    return render(request, 'shops/login.html', locals())

@cookieVerify
def goodsAdd(request):
    doType = ''
    types = Types.objects.all()

    if request.method == 'POST' and request.POST:
        g = Goods()
        g.goods_name = request.POST.get('goodsname')
        g.goods_id = request.POST.get('goodsid')
        g.goods_price = request.POST.get('goodsprice')
        g.goods_now_price = request.POST.get('goodsnowprice')
        g.goods_num = request.POST.get('goodsnum')
        g.goods_description = request.POST.get('goodsdescription')
        g.goods_content = request.POST.get('goodscontent')
        g.types = Types.objects.get(id=int(request.POST.get('goodstypes')))
        g.seller = Seller.objects.get(nickname=request.POST.get('seller'))
        g.save()
        for i in request.FILES.getlist('goodsimages'):
            img = Image()
            img.img_path = 'shops/images/goods/'+i.name #name是文件名，内置方法
            img.img_label = request.POST.get('goodsname')
            img.goods = g
            img.save()

            path = os.path.join(MEDIA_ROOT, 'shops/images/goods/{}'.format(i.name)).replace('\\', '/')
            with open(path, "wb") as f: #wb是以二进制打开
                for j in i.chunks(): #解析图片为二进制文件，全部内容写入到静态文件夹
                    f.write(j)


    return render(request, 'shops/goods_add.html', {'types': types, 'doType': doType})

@cookieVerify
def goodsChange(request, goods_id):
    doType = 'change'
    types = Types.objects.all()
    g = Goods.objects.get(id=int(goods_id))
    if request.method == 'POST' and request.POST:
        g = Goods.objects.get(id=int(goods_id))
        g.goods_name = request.POST.get('goodsname')
        g.goods_id = request.POST.get('goodsid')
        g.goods_price = request.POST.get('goodsprice')
        g.goods_now_price = request.POST.get('goodsnowprice')
        g.goods_num = request.POST.get('goodsnum')
        g.goods_description = request.POST.get('goodsdescription')
        g.goods_content = request.POST.get('goodscontent')
        g.types = Types.objects.get(id=int(request.POST.get('goodstypes')))
        g.seller = Seller.objects.get(nickname=request.POST.get('seller'))
        g.save()
        for i in request.FILES.getlist('goodsimages'):
            img = Image.objects.get(goods=g)
            img.img_path = 'shops/images/goods/'+i.name
            img.img_label = request.POST.get('goodsname')
            img.goods = g
            img.save()
            path = os.path.join(MEDIA_ROOT, 'shops/images/goods/{}'.format(i.name)).replace('\\', '/')
            with open(path, 'wb') as f:
                for j in i.chunks():
                    f.write(j)
    return render(request, 'shops/goods_add.html', {'g': g, 'types': types, 'doType': doType})

@cookieVerify
def goodsList(request):
    goods = Goods.objects.all()
    return render(request, 'shops/goods_list.html', {'goods': goods})

#加密函数
def lockpw(pw):
    md5 = hashlib.md5()
    md5.update(pw.encode())
    result = md5.hexdigest()
    return result

def logout(request):
    response = HttpResponseRedirect(reverse('Shops:login'))
    response.delete_cookie('username')
    del request.session['nickname']
    return response

@cookieVerify
def goodsTypeAdd(request):
    if request.method == 'POST' and request.POST:
        types = Types()
        types.label = request.POST.get('typelabel')
        types.description = request.POST.get('typedescription')
        types.save()
    return render(request, 'shops/goodstype_add.html', locals())

@cookieVerify
def goodsDel(request, goods_id):
    goods = Goods.objects.get(id=goods_id)
    imgs = goods.image_set.all()
    for i in imgs:
        os.remove(os.path.join(MEDIA_ROOT, str(i.img_path).replace('\\', '/')))
    imgs.delete()
    goods.delete()
    return HttpResponseRedirect(reverse('Shops:goodslist'))

@cookieVerify
def goodsDetails(request, goods_id):
    goods = Goods.objects.get(id=goods_id)
    goodsImage = Image.objects.filter(goods=goods)
    return render(request, 'shops/goodsdetails.html', {'goods': goods, 'goodsImage': goodsImage})