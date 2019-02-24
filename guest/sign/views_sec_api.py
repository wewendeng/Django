from django.http import JsonResponse
from sign.models import Event, Guest
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib import auth as django_auth
import base64, time
import hashlib
from django.http import HttpResponse
from Crypto.Cipher import AES
import json

"""
为接口添加安全机制：认证、签名、AES加密
"""

def user_auth(request):
    '''
    用户认证
    :param request:
    :return:
    '''
    get_http_auth = request.META.get('HTTP_AUTHORIZATION', b'')
    auth = get_http_auth.split()
    try:
        auth_parts = base64.b64decode(auth[1]).decode('utf-8').partition(':')
    except IndexError:
        return "null"
    userid, password  = auth_parts[0], auth_parts[2]
    user = django_auth.authenticate(username=userid, password=password)
    if user is not None and user.is_active:
        django_auth.login(request, user)
        return "successs"
    else:
        return "fail"

# 发布会查询接口---添加用户认证
def get_event_list(request):
    auth_result = user_auth(request)
    if auth_result == "null":
        return JsonResponse({"status":"10011", "message":"user auth null"})

    if auth_result == "fail":
        return JsonResponse({"status":"10012", "message":"user auth fail"})

    eid = request.GET.get("eid", "")
    name = request.GET.get("name", "")
    if eid == '' and name == '':
        return JsonResponse({"status":"10021", "message":"parameter error"})

    if eid !='':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({"status":"10022", "status":"query result is empty"})
        else:
            event['eid'] = result.id
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({"status":"200", "message":"successs", "data":event})

    if name != '':
        datas = []
        result = Event.objects.filter(name_contains=name)
        if result:
            for r in result:
                event = {}
                event['eid'] = r.id
                event['name'] = r.name
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
            return JsonResponse({"status":"200", "message":"success", "data":datas})
        else:
            return JsonResponse({"status":"10022", "message":"query result is empty"})


# 用户签名+时间戳
def user_sign(request):

    if request.method == 'POST':
        client_time = request.POST.get("time", "") # 客户端时间戳
        client_sign = request.POST.get("sign", "") # 客户端签名
    else:
        return "error"

    if client_time == '' or client_sign == '':
        return "time or sign null"

    now_time = time.time() # 服务器时间，例：1543564563
    server_time = str(now_time).split('.')[0]
    time_different = int(server_time) - int(client_time) # 获取时间差

    if time_different >= 60:
        return "timeout"

    # 签名检查
    md5 = hashlib.md5()
    sign_str = client_time + "&Guest-Bugmaster"
    sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
    md5.update(sign_bytes_utf8)
    server_sign = md5.hexdigest()
    if server_sign != client_sign:
        return "sign fail"
    else:
        return "sign right"


# 添加发布会接口---增加签名+时间戳
def add_event(request):
    sign_result = user_sign(request)
    if sign_result == "error":
        return JsonResponse({"status":"10011", "message":"request error"})
    if sign_result == "time or sign null":
        return JsonResponse({"status":"10012", "message":"user sign null"})
    if sign_result == "timeout":
        return JsonResponse({"status":"10013", "message":"time or sign null"})
    if sign_result == "sign fail":
        return JsonResponse({"status":"10014", "message":"sign fail"})

    eid = request.POST.get("eid", "")
    name = request.POST.get("name", "")
    limit = request.POST.get("limit", "")
    status = request.POST.get("status", "")
    address = request.POST.get("address", "")
    start_time = request.POST.get("address", "")

    if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
        return JsonResponse({"status":"10021", "message":"parameter value null"})

    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({"status":"10022", "message":"event id already exists"})

    result = Event.objects.filter(name)
    if result:
        return JsonResponse({"status":"10023", "message":"event name already exists"})

    if status == '':
        status =1

    try:
        Event.objects.create(id=eid, name=name, limit=limit, address=address,
                             status = int(status), start_time=start_time)
    except ValidationError:
        error = 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS format'
        return JsonResponse({"status":"10024", "message":error})

    return JsonResponse({"status":"200", "message":"add event success"})


# AES加密算法
BS = 16
unpad = lambda s : s[0: - ord(s[-1])] # 定义unpad函数，输入：s，输出：s[0: - ord(s[-1])

def decryptBase64(src):
    return base64.urlsafe_b64decode(src)

def decryptAES(sec, key):
    '''
    解析AES密文
    '''
    src = decryptBase64(src)
    iv = b"1172311105789011"
    cryptor = AES.new(key, AES.MODE_CBC, iv)
    text = cryptor.decrypt(src).decode()
    return unpad(text)

def aes_encryption(request):

    app_key = "W7v4D60fds2Cmk2U"

    if request.method == 'POST':
        data=request.POST.get("data", "")
    else:
        return "error"

    # 解密
    decode = decryptAES(data, app_key)
    # 转化为字典
    dict_data = json.loads(decode)
    return dict_data

# 嘉宾查询接口---AES算法
def get_guest_list(request):

    dict_data = aes_encryption(request)
    if dict_data == "error":
        return JsonResponse({"status":"10011", "message":"request error"})

    # 取出对应的发布会id和嘉宾手机号
    eid = dict_data['eid']
    phone = dict_data['phone']

    if eid == '':
        return JsonResponse({"status":"10021", "message":"eid cannot be empty"})

    if eid != ''and phont == '':
        datas = []
        results = Guest.objects.filter(event_id=eid)
        if results:
            for r in results:
                guest = {}
                guest['realname'] = r.realname
                guest['phone'] = r.phone
                guest['email'] = r.mail
                guest['sign'] = r.sign
                datas.append(guest)
            return JsonResponse({"status":"200", "message":"success", "data":datas})
        else:
            return JsonResponse({"status":"10022", "message":"quety result is empty"})

    if eid != '' and phone != '':
        guest = {}
        try:
            result = Guest.objects.get(phone=phone, event_id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({"status":"10022", "message":"query result is empty"})
        else:
            guest['realname'] = result.realname
            guest['phone'] = result.phone
            guest['email'] = result.email
            guest['sign'] = result.sign
            return JsonResponse({"status":"200", "message":"success", "data":guest})
