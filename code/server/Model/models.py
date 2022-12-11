from django.db import models

# Create your models here.


class Scene(models.Model):
    sceneNo = models.AutoField(primary_key=True)
    sceneName = models.CharField(max_length=20)
    oriImage = models.URLField()

class Equipment(models.Model):
    name = models.CharField(max_length=20)
    state = models.IntegerField()
    type = models.IntegerField()
    sceneNo = models.IntegerField()

class User(models.Model):
    userName = models.CharField(max_length=20, unique=True)
    phoneNumber = models.CharField(max_length=11, unique=True)
    password = models.CharField(max_length=256)

class UserScene(models.Model):
    sceneNo = models.IntegerField()
    userId = models.IntegerField()