from django import forms


# 表单上传可以使用cleaned_data获取相应input标签的数据，在view里

class UploadFile(forms.Form):
    file_upload = forms.FileField(label='', widget=forms.FileInput(
        attrs={'id':'file_upload','class':"form-control hidden",'onclick':"$('#i-file').click();"}))
