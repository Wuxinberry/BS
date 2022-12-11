"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from . import views, user, scene

urlpatterns = [
    path('admin/', admin.site.urls),
    path('runoob/', views.runoob),
    path('', views.hello),
    path('user/signup', user.signup),
    path('user/login', user.login),
    path('scene/create', scene.create),
    path('scene/equip/add', scene.add_equipment),
    path('scene/equip/edit', scene.edit_equipment),
    path('scene/equip/delete', scene.delete_equipment),
]
