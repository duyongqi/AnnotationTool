from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.core.files import File
from AnnotationTool.settings import MEDIA_ROOT
from .models import myUser, a_text, group, text
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from .form import UploadFile
from django.contrib.auth import logout
from functools import wraps
from .yizhixing import ntree_parser
import json
import os
import dicttoxml
import xmltodict
from xmltodict import _DictSAXHandler
from xml.dom.minidom import parseString
from django.views import View
import xml.etree.ElementTree as ET
from django.utils.decorators import method_decorator
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
    return FileResponse(open((MEDIA_ROOT + '/' + filepath).replace("\\", "/"), 'rb'), as_attachment=True, filename=name,
                        content_type='application/octet-stream')
    # 返回文件到浏览器


@login_required(login_url='/annotation/login/')
def xml_download(request, name):
    # print('hhh')
    user = request.user
    try:
        a_t_object = a_text.objects.get(user=user.myuser, group=user.myuser.group, name=(name.split('.')[0] + '.xml'))
    except:
        a_t_object = None
    if a_t_object:
        path = (MEDIA_ROOT + '/' + a_t_object.xml.name).replace("\\", "/")
        return FileResponse(open(path, 'rb'), as_attachment=True, filename=(name.split('.')[0] + '.xml'),
                            content_type='application/octet-stream')
    else:
        message = '你还未曾提交过标注'
        request.session['message'] = message
        if user.myuser.limits == 0:
            return note(request, name, message)
        else:
            return leader_note(request, name, message)
    # 重定向无法实现，这个方法好像行不通，下载xml不能跳转路由
    # 已经解决，直接调用note 函数再传个参数


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
def note(request, name, args=''):
    if request.method == 'POST':
        # print(request.body.decode('utf-8'))
        # print(request.body)
        # request.body.replace(b'@',b'JJ')
        # print(request.body)
        # request.body.replace(b'JJ', b'@')
        jsondict = json.loads(request.body, encoding='utf-8')
        xml = xmltodict.unparse(jsondict, pretty=True,encoding='utf-8'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  )  # dict转xml
        # xml = dicttoxml.dicttoxml(jsondict, root=False,attr_type=False)
        dom1 = parseString(xml)
        #转化成空行缩进比较合适的形式
        dom= dom1.toprettyxml()
        print(dom)
        try:
            a_text_init = a_text.objects.get(name=name.split('.')[0] + '.xml',
                                             user=request.user.myuser,group=request.user.myuser.group)
        except:
            a_text_init = None
        if a_text_init:
            with open((MEDIA_ROOT + '/' + a_text_init.xml.name).replace('\\','/'),'r+',encoding='utf-8') as file:
                file.truncate()
                file.write(dom)
        else:
            path = (MEDIA_ROOT + '/' + name.split('.')[0] + '.xml').replace('\\', '/')
            # print(path)
            # 以写的形式打开，如果不存在会新建，但是以独写的形式打开如果不存在不会新建，
            # 所以先以写的形式打开，然后写，然后关闭，然后以独写的形式打开，就可以对文本进行读取了
            f = open(path, 'w', encoding='utf-8')
            f.write(dom)
            f.close()
            file_init = open(path, 'r+', encoding='utf-8')
            file = File(file_init, name=name.split('.')[0] + '.xml')
            # print(file.file)
            new_atxt = a_text(name=name.split('.')[0] + '.xml', user=request.user.myuser,
                              group=request.user.myuser.group, xml=file)
            new_atxt.save()
            # print(new_atxt.xml.name)
            file.close()
            os.remove(path)
            #如果从前没有标注过就让文本index加一
            text_init = text.objects.get(name=name,group=request.user.myuser.group)
            text_init.index +=1
            text_init.save()
        return HttpResponseRedirect(reverse('choose_text'))

    # 记住对不同组的判断
    t_object = text.objects.get(name=name, group=request.user.myuser.group)
    file_name = t_object.text.name
    name_input = (MEDIA_ROOT + '/' + file_name).replace("\\", "/")
    with open(name_input,encoding='utf-8') as file_response:
        f_content = file_response.read()
    content = {
        'file_content': f_content,
        'file': t_object,
        'user': request.user,
        'message': args
    }
    return render(request, 'annotation/note.html', content)



class leader_note(View):

    @method_decorator(login_required)
    def get(self,request,name,args=''):
        # #args是xml_download里传来的信息
        # t_object = text.objects.get(name=name, group=request.user.myuser.group)
        # #根据名称和组号获取文件
        # file_name = t_object.text.name
        # name_input = (MEDIA_ROOT + '/' + file_name).replace("\\", "/")
        # #打开文件
        # with open(name_input, encoding='utf-8') as file_response:
        #     f_content = file_response.read()
        # #到这里获取到了text文本，接下来要将xml传给js,等待xml解析
        # annotation_list = a_text.objects.filter(name=name.split('.')[0] + '.xml',group=request.user.myuser.group)
        # print(annotation_list)
        x_object_all = a_text.objects.filter(name=name.split('.')[0] + '.xml',group=request.user.myuser.group)
        t_json = []
        for i in x_object_all:
            # 只有组员的xml会被展示
            if i.user.limits == 0:
                xfile_name = i.xml.name
                xname_input = (MEDIA_ROOT + '/' + xfile_name).replace("\\", "/")
                with open(xname_input, encoding='utf-8') as f:
                    str_xml = f.read()
                str_xml = str_xml.replace('&', '&#38;')  # xml格式不能有"&"符号
                doc = xmltodict.parse(str_xml, encoding='utf-8')
                doc2 = json.dumps(doc, indent=4)
                t_json.append(doc2)
        t_object = text.objects.get(name=name, group=request.user.myuser.group)
        file_name = t_object.text.name
        name_input = (MEDIA_ROOT + '/' + file_name).replace("\\", "/")
        with open(name_input, encoding='utf-8') as file_response:
            f_content = file_response.read()
        content = {
            'file_content': f_content,
            'file': t_object,
            'user': request.user.myuser,
            'message': args,
            't_json': t_json[0]
        }
        return render(request, 'annotation/leader_note.html', content)
    @method_decorator(login_required)
    def post(self,request,name):
        # print(request.body.decode('utf-8'))
        jsondict = json.loads(request.body, encoding='utf-8')
        xml = xmltodict.unparse(jsondict, pretty=True)  # dict转xml
        # xml = dicttoxml.dicttoxml(jsondict, root=False,attr_type=False)
        dom1 = parseString(xml)
        # # print(name)
        dom = dom1.toprettyxml()
        # print(dom)
        print(dom)
        #新建一个组长的标注记录，存储最终标注
        # tree = ET.parse(dom)
        # root = tree.getroot()
        path = (MEDIA_ROOT + '/' +  name.split('.')[0] + '.xml').replace('\\','/')
        print(path)
        #以写的形式打开，如果不存在会新建，但是以独写的形式打开如果不存在不会新建，
        # 所以先以写的形式打开，然后写，然后关闭，然后以独写的形式打开，就可以对文本进行读取了
        f = open(path,'w',encoding='utf-8')
        f.write(dom)
        f.close()
        file_init = open(path,'r+',encoding='utf-8')
        file = File(file_init,name=name.split('.')[0] + '.xml')
        # print(file.readable())
        # print(type(file))
        # file.close()
        # dom.saveXML(path)
        #这里加上的原因是，在之前的upload上面，得到的file是一个'django.core.files.uploadedfile.InMemoryUploadedFile'的class，与user关联
        # 但是在这里，file就是个普通文件，file.name只是个字符串，所以在models里面得不到user的任何信息
        # f_name = (MEDIA_ROOT + '/' + 'xml' + '/' + request.user.myuser.group.group_name + '/' + request.user.myuser.user.username +'/' + file.name.split('/')[-1]).replace('\\','/')
        # print(f_name)
        new_atxt = a_text(name=name.split('.')[0] + '.xml',user=request.user.myuser,group=request.user.myuser.group,xml=file)
        new_atxt.save()
        # print(new_atxt.xml.name)
        file.close()
        os.remove(path)
        remove_text = text.objects.get(name=name,group=request.user.myuser.group)
        remove_text.limit = 0
        remove_text.save()
        xml_list = a_text.objects.filter(name=(name.split('.')[0] + '.xml'), group=request.user.myuser.group)
        for i in xml_list:
            with open((MEDIA_ROOT + '/' + i.xml.name).replace('\\', '/'),'r+',encoding='utf-8') as file_set:
                file_set.truncate()
                dom.encode('utf-8').decode('utf-8')
                file_set.write(dom)
                # file_set.decode('utf-8')
                # print(dom)

        return HttpResponseRedirect(reverse('final_decide'))

# def post(request):
class leader_note1(View):

    @method_decorator(login_required)
    def get(self,request,name,args=''):
        # #args是xml_download里传来的信息
        # t_object = text.objects.get(name=name, group=request.user.myuser.group)
        # #根据名称和组号获取文件
        # file_name = t_object.text.name
        # name_input = (MEDIA_ROOT + '/' + file_name).replace("\\", "/")
        # #打开文件
        # with open(name_input, encoding='utf-8') as file_response:
        #     f_content = file_response.read()
        # #到这里获取到了text文本，接下来要将xml传给js,等待xml解析
        # annotation_list = a_text.objects.filter(name=name.split('.')[0] + '.xml',)
        x_object_all = a_text.objects.filter(name=name.split('.')[0] + '.xml', group=request.user.myuser.group)
        t_json = []
        for i in x_object_all:
            # 只有组员的xml会被展示
            if i.user.limits == 0:
                xfile_name = i.xml.name
                xname_input = (MEDIA_ROOT + '/' + xfile_name).replace("\\", "/")
                with open(xname_input, encoding='utf-8') as f:
                    str_xml = f.read()
                str_xml = str_xml.replace('&', '&#38;')  # xml格式不能有"&"符号
                doc = xmltodict.parse(str_xml, encoding='utf-8')
                doc2 = json.dumps(doc, indent=4)
                t_json.append(doc2)
        t_object = text.objects.get(name=name, group=request.user.myuser.group)
        file_name = t_object.text.name
        name_input = (MEDIA_ROOT + '/' + file_name).replace("\\", "/")
        with open(name_input, encoding='utf-8') as file_response:
            f_content = file_response.read()
        content = {
            'file_content': f_content,
            'file': t_object,
            'user': request.user.myuser,
            'message': args,
            't_json': t_json[1]
        }
        return render(request, 'annotation/leader_note1.html', content)
    @method_decorator(login_required)
    def post(self,request,name):
        # print(request.body.decode('utf-8'))
        jsondict = json.loads(request.body, encoding='utf-8')
        xml = xmltodict.unparse(jsondict, pretty=True)  # dict转xml
        # xml = dicttoxml.dicttoxml(jsondict, root=False,attr_type=False)
        dom1 = parseString(xml)
        # # print(name)
        dom = dom1.toprettyxml()
        # print(dom)
        print(dom)
        #新建一个组长的标注记录，存储最终标注
        # tree = ET.parse(dom)
        # root = tree.getroot()
        path = (MEDIA_ROOT + '/' +  name.split('.')[0] + '.xml').replace('\\','/')
        print(path)
        #以写的形式打开，如果不存在会新建，但是以独写的形式打开如果不存在不会新建，
        # 所以先以写的形式打开，然后写，然后关闭，然后以独写的形式打开，就可以对文本进行读取了
        f = open(path,'w',encoding='utf-8')
        f.write(dom)
        f.close()
        file_init = open(path,'r+',encoding='utf-8')
        file = File(file_init,name=name.split('.')[0] + '.xml')
        # print(file.readable())
        # print(type(file))
        # file.close()
        # dom.saveXML(path)
        #这里加上的原因是，在之前的upload上面，得到的file是一个'django.core.files.uploadedfile.InMemoryUploadedFile'的class，与user关联
        # 但是在这里，file就是个普通文件，file.name只是个字符串，所以在models里面得不到user的任何信息
        # f_name = (MEDIA_ROOT + '/' + 'xml' + '/' + request.user.myuser.group.group_name + '/' + request.user.myuser.user.username +'/' + file.name.split('/')[-1]).replace('\\','/')
        # print(f_name)
        new_atxt = a_text(name=name.split('.')[0] + '.xml',user=request.user.myuser,group=request.user.myuser.group,xml=file)
        new_atxt.save()
        # print(new_atxt.xml.name)
        file.close()
        os.remove(path)
        remove_text = text.objects.get(name=name,group=request.user.myuser.group)
        # print(remove_text[0].limit)
        # remove_text[0].limit = remove_text[0].limit - 1
        # print(remove_text[0].limit)
        # remove_text[0].save()
        #filter数组的0，和get不一样
        remove_text.limit = 0
        remove_text.save()
        xml_list = a_text.objects.filter(name=(name.split('.')[0] + '.xml'), group=request.user.myuser.group)
        for i in xml_list:
            with open((MEDIA_ROOT + '/' + i.xml.name).replace('\\', '/'),'r+',encoding='utf-8') as file_set:
                # print((MEDIA_ROOT + '/' + i.xml.name).replace('\\', '/'))
                file_set.truncate()
                file_set.write(dom)
                # print(dom)

        return HttpResponseRedirect(reverse('final_decide'))



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
        print(type(file))
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
    if request.method == 'POST':
            key = float(request.POST.get('key'))
    else:
        key = 1
    txt_list = text.objects.filter(group=request.user.myuser.group)
    file_list = []
    for t in txt_list:
        if t.index == (request.user.myuser.group.member_number - 1):
            xml_list = a_text.objects.filter(name=(t.name.split('.')[0] + '.xml'), group=request.user.myuser.group)
            xml_path = []
            for x in xml_list:
                #只有组员的标注会被拿去进行一致性判断
                if x.user.limits == 0:
                    xml_path.append(x.xml)
            dex = ntree_parser().same(xml_path)
            print(dex)
            if dex == 1:
                t.limit = 0
                # 删除标注，存储最终标注，直接以组长的身份上传
                if not a_text.objects.filter(user=request.user.myuser,
                                             group=request.user.myuser.group,name=t.name.split('.')[0] + '.xml'):
                    with open((MEDIA_ROOT + '/' + xml_list[0].xml.name).replace('\\','/'),encoding='utf-8') as ff:
                        # print(MEDIA_ROOT + xml_list[0].xml.name)
                        xml_set = str(ff.read())
                    path = (MEDIA_ROOT + '/' + t.name.split('.')[0] + '.xml').replace('\\', '/')
                    f = open(path, 'w', encoding='utf-8')
                    f.write(xml_set)
                    f.close()
                    file_init = open(path, 'r+', encoding='utf-8')
                    file = File(file_init, name=t.name.split('.')[0] + '.xml')
                    new_atxt = a_text(name=t.name.split('.')[0] + '.xml', user=request.user.myuser,
                                      group=request.user.myuser.group, xml=file)
                    new_atxt.save()
                    file.close()
                    os.remove(path)

            if dex >= key and dex < 1 and key!=1:
                file_list.append(t.name)
            if dex == 1 and key == 1:
                file_list.append(t.name)
    return render(request, 'annotation/final_decide.html', {'file_list': file_list})


@login_required(login_url='/annotation/login/')
def logout_view(request):
    # 重定向到homepage
    logout(request)
    return HttpResponseRedirect(reverse('login'))

#
# def set_password(request):
#     return HttpResponse('重置密码界面')
