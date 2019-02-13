from django.http import JsonResponse
from sign.models import Event, Guest


def get_event_list(request):
    '''获取发布会列表'''
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

        print(event_list)
        data = {"status": "110", "massage": "查询成功", "data": event_list}
        return JsonResponse(data)
    else:
        data = {"status": "100", "massage": "请求方法错误"}
        return JsonResponse(data)