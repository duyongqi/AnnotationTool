from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth

# Create your models here.
class myUser(models.Model):
    '''用户表'''
    limits_choices={
        (0,'普通用户'),
        (1,'用户组长'),
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey('group', on_delete=models.CASCADE)
    limits = models.IntegerField(choices=limits_choices , default=0)

    # def __str__(self):
    #     return self.limits


    # class Meta:
    #     ordering = ['user.username']
    #     verbose_name = '用户'
    #     verbose_name_plural = '用户'

class group(models.Model):
    '''小组信息，包括小组成员个数，小组编号'''
    group_name = models.CharField(max_length=50, unique=True)
    member_number = models.IntegerField(default=0)

    def __str__(self):
        return self.group_name

# class text(models.Model):
#     GROUP
#     TEXT

class a_text(models.Model):
    #需要文本名
    name = models.CharField(max_length=50)
    #需要用户的原因：用户重复提交之后的覆盖
    user = models.ForeignKey('myUser', on_delete=models.CASCADE)
    #小组
    group = models.ForeignKey('group', on_delete=models.CASCADE)
    #xml文件
    xml = models.TextField(max_length=500)
    #xml约束文件
    # ttt = models.TextField(max_length=500)



# class a_text(models.Model):
#     '''标注后的xml的表'''
    # name = models.CharField(max_length=50)
#   xml = ...
