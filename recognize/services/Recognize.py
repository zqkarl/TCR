# coding=utf8

from __future__ import division  # 计算浮点
import MySQLdb
import bs4
from bs4 import BeautifulSoup
from recognize.svmutil import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def traversal(soup):

    lines = []
    # 遍历所有节点
    i = 0
    for tag in soup.descendants:
        line = {'sequence': i}
        i += 1
        if type(tag) == bs4.element.Tag:
            try:
                # 标签有内容或者是p标签,并且标签的父节点没有p(因为只需要判断到p就可以了,里面的东西都要的)
                if (tag.string is not None or tag.name == 'p') and tag.find_parent('p') is None:
                    line['content_html'] = str(tag)
                    try:
                        line['content_len'] = len(tag.string.strip())
                    except TypeError and AttributeError:
                        line['content_len'] = 0
                    content = ''
                    for string in tag.stripped_strings:
                        content += string
                    line['content'] = content
                    # content = tag.string
                    line['tag_name'] = tag.name
                    line['tag_id'] = tag.get("id")
                    line['tag_class'] = tag.get("class")

                    # p提取其下所有标签的文字
                    if tag.name == 'p':
                        content = ''
                        for string in tag.stripped_strings:
                            content += string
                        line['content_len'] = len(content.strip())
                        line['content'] = content

            except StopIteration:
                pass

        if type(tag) == bs4.element.NavigableString and tag.string.strip() != '':
            if tag.next_sibling is not None and tag.previous_sibling is not None:
                line['content_html'] = str(tag)+"</br>"
                line['tag_name'] = 'p'
                line['content_len'] = len(unicode(tag).strip())
                content = tag.string
                line['content'] = content

        # 判断该节点是否为需要的节点
        if line.get('tag_name') is not None:
            lines.append(line)  # 在队列尾部插入新数据

    return __recognize(lines, i)


def __recognize(lines, line_max):
    """该方法为处理数据并调用libsvm识别标题和内容"""

    title = ''  # 存放标题
    content = ''  # 存放内容
    content_html = ''  # 存放原生html
    for line in lines:
        # print line.get('content')
        sequence = line.get('sequence')
        tag_name = line.get('tag_name')
        tag_id = line.get('tag_id')
        tag_class = line.get('tag_class')
        content_len = line.get('content_len')

        f1 = sequence / line_max  # 在队列中的顺序

        f2 = 0.5
        try:
            if tag_name.lower() == "h1":
                f2 = 1
            if tag_name.lower() == "h2" or tag_name.lower() == "h3":
                f2 = 0.90
            if tag_name.lower() == "title":
                f2 = 0.80
            if tag_name.lower() == "div":
                f2 = 0.70
            if tag_name.lower() == "span":
                f2 = 0.30
            if tag_name.lower() == "td" or tag_name.lower() == "th":
                f2 = 0.20
            if tag_name.lower() == "strong":
                f2 = 0.15
            if tag_name.lower() == "article":
                f2 = 0.10
            if tag_name.lower() == "p":
                f2 = 0
        except AttributeError:
            pass

        f3 = 0.5
        try:
            if tag_id.lower().find("title") is not -1 or tag_class.lower().find("title") is not -1:
                f3 = 1
            if tag_id.lower().find("headline") is not -1 or tag_class.lower().find("headline") is not -1:
                f3 = 0.90
            if tag_id.lower().find("pic") is not -1 or tag_class.lower().find("pic") is not -1:
                f3 = 0.40
            if tag_id.lower().find("content") is not -1 or tag_class.lower().find("content") is not -1:
                f3 = 0.30
            if tag_id.lower().find("text") is not -1 or tag_class.lower().find("text") is not -1:
                f3 = 0.20
            if tag_id.lower().find("author") is not -1 or tag_class.lower().find("author") is not -1:
                f3 = 0.10
            if tag_id.lower().find("editor") is not -1 or tag_class.lower().find("editor") is not -1:
                f3 = 0
        except AttributeError:
            pass

        f4 = content_len / 100
        if f4 > 1:
            f4 = 1

        data_list = []
        row = "0 1:%f 2:%f 3:%f 4:%f" % (f1, f2, f3, f4)
        # print row
        data_list.append(row)
        y, x = svm_read_problem(data_list)
        m = svm_load_model('model_file')
        p_labs, p_acc, p_vals = svm_predict(y, x, m)
        if p_labs[0] == 1.0:
            title += line.get('content')
        if p_labs[0] == 2.0:
            content += line.get('content')
            content_html += line.get('content_html')

    result = {"title": title, "content": content, "content_html": content_html}
    return result
    # y,x = svm_read_problem('/Users/QISAMA/Documents/PycharmProjects/TCR/recognize/export.txt')
    # prob = svm_problem(y, x)
    # m = svm_train(prob, '-c 8 -g 8')
    # svm_save_model('model_file', m)



