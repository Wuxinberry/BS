from django.http import HttpResponse

from Model.models import Scene
from Model.models import UserScene
from Model.models import Equipment
from server.user import get_equips_by_sid, get_user_scenes_by_uid
import time
import json
import oss2


auth = oss2.Auth('LTAI5tEPrUtaPpbgybxmWT21', 'iPf6OXaKU7JbJzZ8A2bS4Rz0Kx3wE0')
endpoint = 'http://oss-cn-hangzhou.aliyuncs.com'
bucket = oss2.Bucket(auth, endpoint, 'bs-scene-imgs')
BASE_IMG_URL = 'http://bs-scene-imgs.oss-cn-hangzhou.aliyuncs.com/'
headers = dict()
headers['Content-Type'] = 'image/jpg'

def upload_to_oss(userName, sceneName, image):
    imgName = userName+sceneName+str(time.time())+'.jpg'
    image_url = BASE_IMG_URL + imgName
    res = bucket.put_object(imgName, image, headers=headers)
    if res.status == 200:
        return image_url
    else:
        return False

def create(request):
    oriImage = request.FILES.get('oriImage').read()
    data = request.POST
    if Scene.objects.filter(sceneName = data['sceneName']).exists():
         return HttpResponse(json.dumps({'state':1}))  # 场景名已经存在
    oriImageUrl = upload_to_oss(data['userName'], data['sceneName'], oriImage)
    if oriImageUrl == False:
        return HttpResponse(json.dumps({'state': 2}))  # 图片上传失败
    # 创建新场景
    scene = Scene(sceneName=data['sceneName'], oriImage=oriImageUrl)
    scene.save()
    # 保存场景从属关系
    userScene = UserScene(sceneNo=scene.sceneNo, userId=data['uid'])
    userScene.save()
    scenes = get_user_scenes_by_uid(data['uid'])
    return HttpResponse(json.dumps({'state':0, 'sceneData':scenes}))

def edit(request):
    image = request.FILES.get("image").read()
    data = request.POST
    imageUrl = upload_to_oss("", data['sceneNo'], image)
    if imageUrl == False:
        return HttpResponse(json.dumps({'state': 2}))  # 图片上传失败
    Scene.objects.filter(sceneNo=data['sceneNo']).update(oriImage=imageUrl)
    # 返回更新后的场景数据
    return HttpResponse(json.dumps({'imageUrl': imageUrl}))

def add_equipment(request):
    data = json.loads(request.body)
    equipment = Equipment.objects.filter(name=data['name'])
    if equipment.exists():
        return HttpResponse(json.dumps({'state':1})) # 设备名称重复
    # 添加设备
    equipment = Equipment(sceneNo=data['sceneNo'], name=data['name'], state=data['state'], type=data['type'])
    equipment.save()
    equipments = get_equips_by_sid(data['sceneNo'])
    return HttpResponse(json.dumps({'state': 0, 'equipments': equipments}))

def edit_equipment(request):
    data = json.loads(request.body)
    equipment = Equipment.objects.filter(id=data['id'])
    if equipment.exists():
        Equipment.objects.filter(id=data['id']).update(state=data['state'])
        return HttpResponse(json.dumps({'state': 0}))
    return HttpResponse(json.dumps({'state': 1})) # 设备信息上报失败

def delete_equipment(request):
    data = json.loads(request.body)
    Equipment.objects.filter(id=data).delete()
    return HttpResponse(json.dumps({'state': 0}))