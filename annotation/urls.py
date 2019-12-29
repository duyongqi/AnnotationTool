from . import views
from django.urls import path

urlpatterns = [
    path('', views.login, name='homepage'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    # path('set_password', views.set_password,name='set_password'),
    path('choose_text/',views.choose_text,name='choose_text'),
    path('note/',views.note, name='note'),
    path('upload/',views.upload, name='upload'),
    path('final_decide/',views.final_decide, name='final_decide'),
    # path('logout', views.logout, name='logout')
    # path('test/',views.test,name='test')
]