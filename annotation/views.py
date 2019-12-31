from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required

from AnnotationTool.settings import MEDIA_ROOT
from .models import myUser, a_text, group, text
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from .form import UploadFile
import os
from django.contrib.auth import logout
from functools import wraps


# Create your views here.
# 装饰器，只有组长有权限
def leader_required(function):
    @wraps(function)
    def wrapfunction(request, *args, **kwargs):
        if request.user.myuser.limits == 1:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('choose_text'))

    return wrapfunction


@login_required(login_url='/annotation/login/')
@leader_required
def download(request, name):
    user = request.user
    # 获取用户
    filepath = text.objects.get(group=user.myuser.group, name=name).text.name
    # 通过文件名称和文件所在的组获取文件的路径
    # 通过路径打开文件并读取
    return FileResponse(open((MEDIA_ROOT + '/' + filepath).replace("\\", "/"), 'rb'), as_attachment=True, filename=name, content_type='application/octet-stream')
    # 返回文件到浏览器


@login_required(login_url='/annotation/login/')
def xml_download(request, name):
    user = request.user
    try:
        a_t_object = a_text.objects.get(user=user.myuser, group=user.myuser.group, name=name)
    except:
        a_t_object = None
    if a_t_object:
        path = (MEDIA_ROOT + '/' + a_t_object.xml.name).replace("\\", "/")
        return FileResponse(open(path, 'rb'), as_attachment=True, filename=name)
    else:
        message = '你还未曾提交过标注'
        request.session['message'] = message
        return note(request,name,message)
    #重定向无法实现，这个方法好像行不通，下载xml不能跳转路由
    #已经解决，直接调用note 函数再传个参数

# 登录
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # 注意：这里不能用user.objects.get或者filter，因为密码加密，验证不了，得用authenticate
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('choose_text'))
        else:
            content = {
                'message': '用户名或密码错误',
            }
            return render(request, 'annotation/login.html', content)
    return render(request, 'annotation/login.html')


def register(request):
    group_list = group.objects.all()
    status = None
    # 状态变量初值
    if request.method == 'POST':
        # 获取表单内容
        username = request.POST.get('username', '')
        group_name = request.POST.get('group_name', '')
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        # 判断状态并给状态变量赋相应的值

        # 如果密码为空
        if password == '' or repeat_password == '':
            status = 'empty'
        # 如果两个密码不一致
        elif password != repeat_password:
            status = 'repeat_error'
        else:
            try_user = User.objects.filter(username=username)
            if try_user:
                status = 'user_exist'
                # return HttpResponse(content=username)
            # 新建auth中的user实体
            else:
                new_user = User.objects.create_user(username=username, password=password)
                new_user.save()
                # 通过组号获取小组
                group_1 = group.objects.get(group_name=group_name)
                # 新建用户
                new_myUser = myUser(user=new_user, group=group_1)
                new_myUser.save()
                # 小组成员个数加1
                group_1.member_number += 1
                group_1.save()
                return HttpResponseRedirect(reverse('login'))
    content = {
        'status': status,
        'group_list': group_list,
    }
    # 向html传递参数
    return render(request, 'annotation/register.html', content)


# 用户以及用户组长文本选择（暂定为同一个界面）
@login_required(login_url='/annotation/login/')
def choose_text(request):
    user = request.user
    text_list = text.objects.filter(group=user.myuser.group)
    content = {
        'user': request.user,
        'text_list': text_list,
    }
    return render(request, 'annotation/choose_text.html', content)


# 用户标注界面
@login_required(login_url='/annotation/login/')
def note(request, name,args=''):
    # 记住对不同组的判断
    t_object = text.objects.get(name=name, group=request.user.myuser.group)
    file_name = t_object.text.name
    name_input = (MEDIA_ROOT + '/' + file_name).replace("\\", "/")
    with open(name_input, encoding='utf-8') as file_response:
        f_content = file_response.read()
    content = {
        'file_content': f_content,
        'file': t_object,
        'user': request.user,
        'message': args
    }
    return render(request, 'annotation/note.html', content)


# 组长上传界面
@leader_required
@login_required(login_url='/annotation/login/')
def upload(request):
    if request.method == "POST":
        # 获取上传的表单
        form = UploadFile(request.FILES)
        # 获取用户
        user = request.user
        # 获取文件
        file = request.FILES['file_upload']
        message = '上传成功'
        if form.is_valid:
            # group_name = user.myuser.group.group_name
            # group_in = group.objects.get(group_name=group_name)
            if text.objects.filter(name=file.name, group=user.myuser.group):
                message = '文件已经存在'
                form = UploadFile()
                return render(request, 'annotation/upload.html', {'form': form, 'message': message})
            new_text = text(name=file.name, group=user.myuser.group, text=file)
            # 注意这里的user.myuser.group,我发现request里面包括user，myuser就是存在数据库的那个
            new_text.save()
            form = UploadFile()
            return render(request, 'annotation/upload.html', {'form': form, 'message': message})
        else:
            form = UploadFile()
            message = '上传失败'
            return render(request, 'annotation/upload.html', {'form': form, 'message': message})
    form = UploadFile()
    return render(request, 'annotation/upload.html', {'form': form})


# 组长最终决定标注界面
@leader_required
@login_required(login_url='/annotation/login/')
def final_decide(request):
    # 首先通过组名查找所有上传过的文本，因为用户每提交一次标注，文本的index值会加一，所以可以通过判断index的值，确定是否在页面中显示出来
    file_list = text.objects.filter(group=request.user.myuser.group)
    return render(request, 'annotation/final_decide.html', {'file_list': file_list, 'user': request.user})


@login_required(login_url='/annotation/login/')
def logout_view(request):
    # 重定向到homepage
    logout(request)
    return HttpResponseRedirect(reverse('login'))

#
# def set_password(request):
#     return HttpResponse('重置密码界面')
