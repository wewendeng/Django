from django.urls import path

import views_sec_api
from sign import views_api
from sign.views_sec_api import get_event_list, add_event, get_guest_list


urlpatterns = [
    path('get_event_list/', views_api.get_event_list),
    path('add_event/', views_api.add_event),
    path('get_guest_list/', views_api.get_guest_list),
    path('add_guest/', views_api.add_guest),
    path('user_sign/', views_api.user_sign),
    path('sec_get_event_list/', views_sec_api.get_event_list,),
    path('sec_add_event/', views_sec_api.add_event,),
    path('get_guest_list', views_sec_api.get_guest_list),
]