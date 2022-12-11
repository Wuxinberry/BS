from django.http import HttpResponse

from Model.models import User
from Model.models import Scene
from Model.models import UserScene
from Model.models import Equipment
import json
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

def signup(request):
    data = json.loads(request.body)
    # 判断用户名和电话号码是否唯一
    userNameCount = User.objects.filter(userName=data['userName'])
    if userNameCount.exists():  # 用户名已存在
        return HttpResponse(json.dumps({'state': 1}))
    phoneNumberCount = User.objects.filter(phoneNumber=data['phoneNumber'])
    if phoneNumberCount.exists():  # 手机号已存在
        return HttpResponse(json.dumps({'state': 2}))
    # 插入新用户
    user = User(userName=data['userName'], phoneNumber=data['phoneNumber'], password=make_password(data['password1']))
    user.save()

    # 返回注册结果
    res = json.dumps({'state': 0})
    return HttpResponse(res)


def login(request):
    data = json.loads(request.body)
    user = User.objects.filter(userName=data['userName'])
    if user.exists():     # 用户名存在
        # 密码匹配
        print(make_password(data['password']))
        if check_password(data['password'], user[0].password):
            id = user[0].id
            scenes = get_user_scenes_by_uid(id)
            return HttpResponse(json.dumps({'state':0, 'id': id, 'sceneData':scenes})) # 成功登录
        return HttpResponse(json.dumps({'state':2})) # 密码不正确
    return HttpResponse(json.dumps({'state':1})) # 用户不存在

def get_user_scenes_by_uid(uid):
    scenes = UserScene.objects.filter(userId=uid)
    if scenes.exists():
        res = []
        for item in scenes:
            scene = Scene.objects.get(sceneNo=item.sceneNo)
            equips = get_equips_by_sid(item.sceneNo)
            sceneDict = {'sceneName': scene.sceneName, 'sceneNo': scene.sceneNo, 'oriImage': scene.oriImage, 'equipments': equips}
            res.append(sceneDict)
        print(res)
        return res
    return []

def get_equips_by_sid(sid):
    equips = Equipment.objects.filter(sceneNo=sid)
    if equips.exists():
        res = []
        for item in equips:
            type = ""
            if item.type == 1:
                type = "灯"
            elif item.type == 2:
                type = "温度计"
            elif item.type == 3:
                type = "湿度计"
            elif item.type == 4:
                type = "门锁"
            elif item.type == 5:
                type = "开关"
            equipDict = {'name': item.name, 'state': item.state, 'id': item.id, 'type': type}
            print(equipDict)
            res.append(equipDict)
        return res
    return []