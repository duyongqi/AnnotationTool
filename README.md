# AnnotationTool
系统运行须知：
!!! important !!!（也可以参考django官方文档了解数据库迁移的知识和admin页面的实现）

1. Django版本3.0.1，python版本3.7，

2. 本系统使用python自带的sqlite数据库，如果想修改为使用其他数据库请关注setting.py文件的database选项，参考https://docs.djangoproject.com/en/3.0/ref/databases/
 
3. 使用本系统需要在激活python虚拟环境后，在命令行执行：
py manage.py makemigrations
py manage.py migrate

********执行了23两步，至此完成数据库的映射和迁移

4. 创建superuser，在命令行执行:
py manage.py createsuperuser 

5. 在命令行里输入py manage.py runserver 运行系统

6. 你就可以在127.0.0.1:8000/annotation看到我们的注册登录界面了

7. 127.0.0.1:8000/admin是管理员界面，登录信息是你第4步填写的superuser信息

# AnnotationTool
text annotation tool
1.标注时，请先标触发事件（鞠躬：））
2.提交标注时由于编码问题，请提交两次（鞠躬：））


