"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sign import views  # 导入sign应用views文件

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index), # 添加index/路径配置
    path('login_action/',views.login_action), # 添加登录处理路径配置
    path('event_manage/',views.event_manage), # 添加发布会管理路径配置
    path('accounts/login/',views.index), # 添加找不到路径的情况默认跳转登录路径配置
]
