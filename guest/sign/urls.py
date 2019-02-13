from django.urls import path
from sign import views_api


urlpatterns = [
    path('get_event_list/', views_api.get_event_list, name='get_event_list')
]