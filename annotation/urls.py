from . import views
from django.urls import path

urlpatterns = [
    path('', views.login, name='homepage'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    # path('set_password', views.set_password,name='set_password'),
    path('choose_text/',views.choose_text,name='choose_text'),
    path('note/<name>/',views.note, name='note'),
    path('leader_note/<name>/', views.leader_note.as_view(), name='leader_note'),
    path('upload/',views.upload, name='upload'),
    path('download/<name>/', views.download, name='download'),
    path('xml_download/<name>/', views.xml_download, name='xml_download'),
    path('final_decide/',views.final_decide, name='final_decide'),
    path('logout/', views.logout_view, name='logout')
    # path('test/',views.test,name='test')
]