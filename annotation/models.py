from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth


# Create your models here.
def text_path(instance, filename):
    # return the whole path to the file
    return "{0}/{1}/{2}".format('text',instance.group.group_name,  filename)


class myUser(models.Model):
    '''用户表'''
    limits_choices = {
        (0, '普通用户'),
        (1, '用户组长'),
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey('group', on_delete=models.CASCADE)
    limits = models.IntegerField(choices=limits_choices, default=0)

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
    # 需要文本名
    name = models.CharField(max_length=50)
    # 需要用户的原因：用户重复提交之后的覆盖
    user = models.ForeignKey('myUser', on_delete=models.CASCADE)
    # 小组
    group = models.ForeignKey('group', on_delete=models.CASCADE)
    # xml文件
    xml = models.TextField(max_length=500)
    # xml约束文件
    # ttt = models.TextField(max_length=500)


class text(models.Model):
    # 文本名
    name = models.CharField(max_length=50)
    group = models.ForeignKey('group', on_delete=models.CASCADE)
    # 文本内容或者文本地址，未定
    text = models.FileField(upload_to=text_path)
    # 文本标注次数
    index = models.IntegerField(default=0)
    # 文本是否可以被普通用户标注
    limit = models.IntegerField(default=1)
# class a_text(models.Model):
#     '''标注后的xml的表'''
# name = models.CharField(max_length=50)
#   xml = ...
