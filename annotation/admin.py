from django.contrib import admin
from .models import myUser,group,a_text
# Register your models here.

admin.site.register(myUser)
admin.site.register(group)
admin.site.register(a_text)

