from django.http import JsonResponse
from sign.models import Event, Guest
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.db.utils import IntegrityError
import json
from json import JSONDecodeError
import time


def get_event_list(request):
    '''
    获取发布会列表
    :param request
    :return
    '''
    if request.method == 'GET':
        events = Event.objects.all()
        event_list = []

        for event in events:
            event_dict = {
                "id": event.id,
                "name": event.name,
                "limit": event.limit,
                "status": event.status,
                "address": event.address,
                "start_time": event.start_time,
            }
            event_list.append(event_dict)

        data = {"status":"110", "message":"查询成功", "data": event_list}
        return JsonResponse(data)
    else:
        data = {"status":"100", "message":"请求方法错误"}
        return JsonResponse(data)

def add_event(request):
    '''
    添加发布会
    :param request
    :return
    '''

    #eid = request.POST.get("id", "")
    #name = request.POST.get("name", "")
    #limit = request.POST.get("limit", "")
    #status = request.POST.get("status", "")
    #address = request.POST.get("address", "")
    #start_time = request.POST.get("start_time", "")

    if request.method == 'POST':
        try:
            event_dict = json.loads(request.body)
        except JSONDecodeError:
            return JsonResponse({"status":"201", "message":"参数不是JSON格式"})
        try:
            eid = event_dict["id"]
            name = event_dict["name"]
            limit = event_dict["limit"]
            status = event_dict["status"]
            address = event_dict["address"]
            start_time = event_dict["start_time"]
        except KeyError:
            return JsonResponse({"status":"202", "message":"必传参数key不能为空"})

        if eid == "" or name == "" or limit == "" or start_time == "" or address == "":
            return JsonResponse({"status":"101", "message":"必传参数value为空"})
        try:
            id_int = int(eid)
        except ValueError:
            return JsonResponse({"status":"103", "message":"发布会id类型错误"})

        event = Event.objects.filter(id=id_int)
        print(event)
        if event:
            return JsonResponse({"status":"102", "message":"发布会id已经存在"})

        event =  Event.objects.filter(name=name)
        if event:
            return JsonResponse({"status":"104", "message":"发布会名称已存在"})

        if status == '':
            status = 1

        try:
            Event.objects.create(id=eid, name=name, limit=limit, address=address,
                                 status=int(status), start_time=start_time)
        except ValidationError:
            error = "日期格式错误.格式：YYYY-MM-DD HH:MM:SS."
            return JsonResponse({"status":"105", "message":error})

        return JsonResponse({"status":"200", "message":"创建成功"})

    else:
        data = {"status":"100", "message":"请求方法错误"}
        return JsonResponse(data)


def get_guest_list(request):
    '''
    获取嘉宾列表
    :param request
    :return
    '''

    if request.method == 'GET':
        guests = Guest.objects.all()
        guest_list = []
        for guest in guests:
            guest_list.append(model_to_dict(guest))
        return JsonResponse({"status":"201", "message":"查询成功",
                             "data": guest_list})
    else:
        return JsonResponse({"status":"404", "message":"请求方法错误"})

def add_guest(request):
    '''
    获取嘉宾列表
    :param request
    :return
    '''

    if request.method == 'POST':

        try:
            event_dict = json.loads(request.body)
        except JSONDecodeError:
             return JsonResponse({"status":"101", "message":"parameter not json format"})
        try:
            eid = event_dict["eid"]
            realname = event_dict["realname"]
            phone = event_dict["phone"]
            email = event_dict["email"]
        except KeyError:
            return JsonResponse({"status":"10020", "message":"parameter key null"})

        if eid == '' or realname == '' or phone == '':
            return JsonResponse({"status":"10021", "message":"parameter value null"})

        result = Event.objects.filter(id=eid)
        if not result:
            return JsonResponse({"status":"10022", "message":"event id null"})

        result = Event.objects.get(id=eid).status
        if not result:
            return JsonResponse({"status":"10023",
                                  "message":"event status is not available"})

        event_limit = Event.objects.get(id=eid).limit
        guest_limit =Guest.objects.filter(event_id=eid)
        if len(guest_limit) >= event_limit:
            return JsonResponse({"status":"10024", "message":"event number is full"})

        event_time = Event.objects.get(id=eid).start_time  # 发布会时间
        etime = str(event_time).split('+')[0]
        timeArray = time.strptime(etime, "%Y-%m-%d %H:%M:%S")
        e_time = int(time.mktime(timeArray))
        n_time = int(time.time())
        if n_time >= e_time:
            return JsonResponse({"status":"10025", "message":"event has started"})

        try:
            Guest.objects.create(realname=realname, phone=phone, email=email,
                                  sign=0,event_id=eid)
        except IntegrityError:
            return JsonResponse({"status":"10026",
                                  "message":"the event guest phone number repeat"})

        return JsonResponse({"status":"200", "message":"add guest success"})
    else:
        data = {"status":"100", "message":"请求方法错误"}
        return JsonResponse(data)

def user_sign(request):
    '''
    用户签到接口
    :param request
    :return
    '''

    if request.method == 'POST':
        #eid = request.POST.get('eid', '')
        #phone = request.POST.get('phone', '')
        event_dict = json.loads(request.body)
        eid = event_dict["id"]
        phone = event_dict["phone"]

        if eid == '' or phone == '':
            return JsonResponse({"status":"10021", "message":"parameter error"})

        result = Event.objects.filter(id=eid)
        if not result:
            return JsonResponse({"status":"10022", "message":"event id null"})

        result = Event.objects.get(id=eid).status
        if not result:
            return JsonResponse({"status":"10023",
                                 "message":"event status is not available"})

        event_time = Event.objects.get(id=eid).start_time
        etime = str(event_time).split('+')[0]
        timeArray = time.strptime(etime, "%Y-%m-%d %H:%M:%S")
        e_time = int(time.mktime(timeArray))
        n_time = int(time.time())
        if n_time >= e_time:
            return JsonResponse({"status": "10024", "message": "event has started"})

        result = Guest.objects.filter(phone=phone)
        if not result:
            return JsonResponse({"status":"10025", "message":"user phone is null"})

        result = Guest.objects.filter(phone=phone, event_id=eid)
        if not result:
            return JsonResponse({"status":"10026",
                                 "message":"user did not participate in the conference"})

        result = Guest.objects.get(event_id=eid, phone=phone).sign
        if result:
            return JsonResponse({"status":"10027", "message":"user has sign in"})
        else:
            Guest.objects.filter(phone=phone).update(sign='1')
            return JsonResponse({"status":"200", "message":"sign successs"})
    else:
        data = {"status": "100", "message": "请求方法错误"}
        return JsonResponse(data)