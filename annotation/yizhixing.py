from AnnotationTool.settings import MEDIA_ROOT
# # from .models import a_text
import xml.etree.ElementTree as ET


# import xml.dom.minidom
# #!/usr/bin/python
# # -*- coding: UTF-8 -*-
# # 1.首先查询数据库获取同一组的所有标注
# # path = a_text.objects.filter(group=user.myuser.group,name=name)

# 把3重列表里面的二重列表中同一位置的元素拿出来存成一个数组
def three_to_one(listlist, index1, index2=None):
    one = []
    if index2 != None:
        for i in range(len(listlist)):
            one.append(listlist[i][index1][index2])
    else:
        for i in range(len(listlist)):
            one.append(len(listlist[i][index1]))
    one.sort()
    return one


class parser():
    def parser_xml(self, xml):
        tree = ET.parse((MEDIA_ROOT + '/' + xml.name).replace('\\','/'))
        root = tree.getroot()
        # 最终返回的数组
        parse_string = []
        # 遍历所有事件
        for child in root:
            # 用来存储每个事件
            event = [child.attrib['TYPE']]
            # 数组第一位是事件类型
            for children in child:
                position = [int(children.attrib['START']), int(children.attrib['END'])]
                event.append(position)
            # 将事件添加到数组里，所以最后生成的是一个所有事件组成的二位列表，列表中的每一个列表
            # 中的第一个是事件类型，第二个是触发事件，后面的是所有的事件参数，除了第一个是字符串，其他的村的都是起始位置构成的数组，所以目前是个三维列表
            parse_string.append(event)
        return parse_string


# if __name__ == '__main__':
#     p = parser()
#     list = p.parser_xml('aa.xml')
#     print(list)
class ntree_parser(parser):
    # 判断一致性
    def same(self, path_list):
        if path_list == None:
            dex = 0
            return dex
        dex = 0
        # 把所有的解析后生成的数组放在一起，放在tree里
        tree = []
        one_tree_length = []
        leng_input = len(path_list)
        for i in range(leng_input):
            tree.append(parser().parser_xml(path_list[i]))
            # print(len(tree[i]))
        # print(tree)

        # 判断，如果大家标注的事件个数都不一样，一致性直接0
        for i in range(leng_input):
            one_tree_length.append(len(tree[i]))
        one_tree_length.sort()
        if one_tree_length[0] != one_tree_length[leng_input - 1]:
            dex = 0
            return dex

        # 根据事件个数确定循环的次数,每次循环判断一个事件的一致性
        for i in range(one_tree_length[0]):
            # 如果事件不一致，一致性也为0
            type = three_to_one(tree, i, 0)
            # print(type)
            if type[0] != type[leng_input - 1]:
                dex = 0
                return dex

            # 如果事件参数个数不一致，一致性同样为0
            number_of_argument = three_to_one(tree, i)
            # print(number_of_argument)
            if number_of_argument[0] != number_of_argument[leng_input - 1]:
                dex = 0
                return dex

            # 下面开始计算一致性
            # 到这里，所有文本标注的事件个数一相同，每个事件的事件类型，参数个数也相同，
            # 根据每棵树的长度确定下一层对事件参数的循环次数
            dex_argument = 0
            for j in range(1, number_of_argument[0]):
                argument = three_to_one(tree, i, j)
                # 这里我还没决定要不要丢掉奇异的
                # print(argument)
                left_min = int(argument[0][0])
                left_max = int(argument[leng_input - 1][0])
                # print(left_min, left_max, 'left')
                # 翻转的目的是方便以END值为key排序（说法不严谨，意思是这样）
                for a in argument:
                    a.reverse()
                argument.sort()
                right_min = int(argument[0][0])
                right_max = int(argument[leng_input - 1][0])
                # print(right_min, right_max, 'right')
                if right_min < left_max:
                    dex_argument = dex_argument + 0
                    # print(dex_argument, 'hhhhhhh')
                else:
                    # 获得一个标签的一致性
                    dex_argument = dex_argument + (right_min - left_max + 1) / (right_max - left_min + 1)
                    # print(dex_argument, 'bbbbbbb')
            # 获得一个事件的一致性,就是计算每个标签一致性的平均值
            dex_argument = dex_argument / (number_of_argument[0] - 1)
            # print(dex_argument)
            dex = dex + dex_argument
            # print(dex)
        dex = dex / one_tree_length[0]
        return dex
# if __name__ == '__main__':



# class atext(ntree_parser):
#     def yizhi(self,pathlist,request):





