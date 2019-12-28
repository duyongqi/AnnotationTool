from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import myUser, a_text, group
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate



# Create your views here.
# 首页
def homepage(request):
    return render(request, 'annotation/homepage.html')


# 登录
def login(request):
    # user = request.user
    # content = {
    #     'user': user
    # }
    # 使用auth自带的验证函数
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('choose_text'))

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # 注意：这里不能用user.objects.get或者filter，因为密码加密，验证不了，得用authenticate
        if authenticate(username=username, password=password):
            return HttpResponseRedirect(reverse('choose_text'))
        else:
            content ={
                'message': '用户名或密码错误',

            }
            return render(request,'annotation/login.html', content)
    return render(request, 'annotation/login.html')


# 注册
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
        'group_list' : group_list,
    }
    # 向html传递参数
    return render(request, 'annotation/register.html', content)


# 用户以及用户组长文本选择（暂定为同一个界面）
def choose_text(request):
    return render(request, 'annotation/choose_text.html')


# 用户标注界面
def note(request):
    return render(request, 'annotation/note.html')


# 组长上传界面
def upload(request):
    return render(request, 'annotation/upload.html')


# 组长最终决定标注界面
def final_decide(request):
    return render(request, 'annotation/final_decide.html')


def logout(request):
    # 重定向到homepage
    return HttpResponse('重定向到主界面，还没实现')


def set_password(request):
    return HttpResponse('重置密码界面')
