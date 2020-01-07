import xmltodict, json
from AnnotationTool.settings import MEDIA_ROOT
with open((MEDIA_ROOT + '/xml/2/csrf/bb.xml' ).replace("\\", "/"),'r',encoding='utf-8') as f:
    str_xml = str(f.read())
    # print(str_xml)

str_xml = str_xml.replace('&','&#38;')  # xml格式不能有"&"符号
# print('jjjj')
doc = xmltodict.parse(str_xml,encoding='utf-8')
# doc1 = json.load(doc)
# load可以实现中文显示
# print('kkkk')
# json.loads() # 将json数据转化成dict数据
# json.dumps() # 将dict数据转化成json数据
# json.load() # 读取json文件数据，转成dict数据
# json.dump() # 将dict数据转化成json数据后写入json文件
j = json.dumps(doc,indent=4, ensure_ascii=False)
print(j)