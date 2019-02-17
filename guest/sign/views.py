from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse


# Create your views here.



def index(request):
    return render(request,"index.html")

# 登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username = username,password = password)
        if username == '' or password == '':
            return render(request, 'index.html', {'error':'username or password null'})

        if user is not None:
            auth.login(request, user)    # 登录
            repose = HttpResponseRedirect( '/event_manage/')
            # repose.set_cookie('user', username, 3600)   # 添加浏览器cookies
            request.session['user'] = username            # session信息记录到浏览器
            return repose
        else:
            return render(request, 'index.html', {'error':'username or password is error!'})
    return render(request, 'index.html')

# 退出登录
@ login_required
def logout(request):
    auth.logout(request) #退出登录
    response = HttpResponseRedirect('/index/')
    return response


# 发布会管理
@ login_required
def event_manage(request):
    event_list = Event.objects.all()
    # user_cookie = request.COOKIES.get('user','')   # 获取浏览器的cookie
    user_cookie = request.session.get('user','')     # 读取浏览器session
    return render(request, 'event_manage.html', {"user":user_cookie,
                                                 "events":event_list})
# 发布会名称搜索
def search_name(request):
    if request.method == 'POST':
        user_cookie = request.session.get('user', '')
        name = request.GET.get("event_name", "")
        event_list = Event.objects.filter(name__contains=name)
        return render(request, "event_manage.html", {"user":user_cookie,
                                                     "events":event_list})
    else:
        return HttpResponse("404")

# 嘉宾管理
def guest_manage(request):
    #if request.method == "POST":
    user_cookie = request.session.get('username', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整数，则返回第一页数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出9999，则返回最后一页数据
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user":user_cookie,
                                                  "guests":contacts})
    #else:
       # return HttpResponse("404")

# 签到页面
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.all()
    guest_data = str(len(guest_list)) # 签到人数
    sign_data = 0 # 已签到人数
    for guest in guest_list:
        if guest.sign == 1:
            sign_data +=1
    return render(request, 'sign_index.html', {'event': event,
                                               'guest':guest_data,
                                               'sign':sign_data})

# 签到动作
def sign_index_action(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        guest_list = Guest.objects.filter(event_id=event_id)
        guest_data = str(len(guest_list))
        sign_data = 0
        for guest in guest_list:
            if guest.sign == True:
                sign_data += 1

        phone = request.POST.get('phone','')

        result = Guest.objects.filter(phone=phone)
        if not result:
            return render(request, 'sign_index.html',
                          {'event':event, 'hint':'Phone error', 'guest':guest_data, 'sign':sign_data})

        result = Guest.objects.filter(phone=phone, event_id=event_id)
        if not result:
            return render(request, 'sign_index.html',
                          {'event':event, 'hint':'Event or Phone error', 'guest':guest_data, 'sign':sign_data})

        result = Guest.objects.get(event_id=event_id, phone=phone)
        if result.sign:
            return render(request, 'sign_index.html',
                          {'event':event, 'hint':'User has sign in', 'guest':guest_data, 'sign':sign_data})
        else:
            Guest.objects.filter(event_id=event_id, phone=phone).update(sign='1')
            return render(request, 'sign_index.html',
                          {'event':event, 'hint':'Sign in success!',
                           'user':result, 'guest':guest_data, 'sign':str(int(sign_data)+1)})
    else:
        return HttpResponse('404')


def api_test(request):
    '''接口测试'''
    data = {"message":"请求成功",
            "data":{"id":"123", "name":"tom"}}
    return JsonResponse(data)