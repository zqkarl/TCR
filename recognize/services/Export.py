# -*- coding: UTF-8 -*-
from __future__ import division
import MySQLdb
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def export2txt():
    db = MySQLdb.connect("qisama.me",
                         "root",
                         "smghd",
                         "svm",
                         charset="utf8")
    cursor = db.cursor()

    txt = open("/Users/QISAMA/Desktop/export.txt", "a+")

    sql = 'SELECT * FROM url_analyses'

    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        result = row[1]
        f1 = row[2]
        f2 = row[3]
        f3 = row[4]
        f4 = row[5]
        f5 = row[6]
        f6 = row[7]
        f7 = row[8]

        if result == 3:
            result = 1

        f4d = -1
        if f4.find("other") is not -1:
            f4d = 90
        if f4.find("null") is not -1:
            f4d = 60
        if f4.find("list") is not -1:
            f4d = 40
        if f4.find("article") is not -1:
            f4d = 33
        if f4.find("content") is not -1:
            f4d = 25
        if f4.find("blog") is not -1:
            f4d = 20
        if f4.find("index") is not -1:
            f4d = 10
        if f4.find("default") is not -1:
            f4d = 5
        if f4.find("class") is not -1:
            f4d = 0

        f5d = 0
        if f5.lower().find("html") is not -1:
            f5d = 80
        if f5.lower().find("null") is not -1:
            f5d = 65
        if f5.lower().find("jsp") is not -1:
            f5d = 40
        if f5.lower().find("asp") is not -1:
            f5d = 20
        if f5.lower().find("php") is not -1:
            f5d = 20
        if f5.lower().find("aspx") is not -1:
            f5d = 20
        if f5.lower() is 'other':
            f5d = 0

        if result != 0:
            print "%d 1:%d 2:%d 3:%d 4:%d %s 5:%d %s 6:%d 7:%d \n" % (result,f1, f2, f3, f4d, f4, f5d, f5,f6, f7)
            txt.write("%d 1:%d 2:%d 3:%d 4:%d 5:%d 6:%d 7:%d \n" % (result,f1, f2, f3, f4d, f5d, f6, f7))
    txt.close()


def exporthtml2txt():
    db = MySQLdb.connect("qisama.me",
                         "root",
                         "smghd",
                         "svm",
                         charset="utf8")
    cursor = db.cursor()
    txt = open("/Volumes/mobile/export.txt", "a+")
    for i in range(1, 45):
        sql = 'SELECT * FROM content_info WHERE url_id = %d' % i
        cursor.execute(sql)
        results = cursor.fetchall()
        len_ = len(results)
        max_s = results[len_-1][3]
        for row in results:
            result = row[1]
            squence = row[3]
            f1 = squence/max_s

            f2 = 0.5
            tag = row[4]
            try:
                if tag.lower() == "h1":
                    f2 = 1
                if tag.lower() == "h2" or tag.lower() == "h3":
                    f2 = 0.90
                if tag.lower() == "title":
                    f2 = 0.80
                if tag.lower() == "div":
                    f2 = 0.70
                if tag.lower() == "span":
                    f2 = 0.30
                if tag.lower() == "td" or tag.lower() == "th":
                    f2 = 0.20
                if tag.lower() == "strong":
                    f2 = 0.15
                if tag.lower() == "article":
                    f2 = 0.10
                if tag.lower() == "p":
                    f2 = 0
            except AttributeError:
                pass

            tag_id = row[5]
            tag_class = row[6]
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

            f4 = row[7] / 100
            if f4 > 1:
                f4 = 1

            # content = row[8]
            # f5 = 50
            # try:
            #     if content.find("记者") is not -1:
            #         f5 = 15
            #     if content.find("编辑") is not -1 or content.find("撰文") is not 1:
            #         f5 = 10
            #     if content.find("原标题") is not -1:
            #         f5 = 0
            # except AttributeError:
            #     pass

            print "%d 1:%f 2:%f 3:%f 4:%f \n" % (result, f1, f2, f3, f4)
            # if random.randint(0, 1) == 1 or result != 0:
            txt.write("%d 1:%f 2:%f 3:%f 4:%f \n" % (result, f1, f2, f3, f4))


def exporthtml2txt_out(id_):
    db = MySQLdb.connect("qisama.me",
                         "root",
                         "smghd",
                         "svm",
                         charset="utf8")
    cursor = db.cursor()
    txt = open("/Volumes/mobile/content_test.txt", "a+")
    show_ = open("/Volumes/mobile/show%d.txt" % id_, "a+")
    sql = 'SELECT * FROM content_info_copy WHERE url_id = %d' % id_
    cursor.execute(sql)
    results = cursor.fetchall()
    len_ = len(results)
    max_s = results[len_-1][3]
    for row in results:
        result = row[1]
        squence = row[3]
        f1 = squence/max_s

        f2 = 0.5
        tag = row[4]
        try:
            if tag.lower() == "h1":
                f2 = 1.0
            if tag.lower() == "h2" or tag.lower() == "h3":
                f2 = 0.90
            if tag.lower() == "title":
                f2 = 0.80
            if tag.lower() == "div":
                f2 = 0.70
            if tag.lower() == "span":
                f2 = 0.30
            if tag.lower() == "td" or tag.lower() == "th":
                f2 = 0.20
            if tag.lower() == "strong":
                f2 = 0.15
            if tag.lower() == "article":
                f2 = 0.1
            if tag.lower() == "p":
                f2 = 0
        except AttributeError:
            pass

        tag_id = row[5]
        tag_class = row[6]
        f3 = 0.5
        try:
            if tag_id.lower().find("title") is not -1 or tag_class.lower().find("title") is not -1:
                f3 = 1
            if tag_id.lower().find("headline") is not -1 or tag_class.lower().find("headline") is not -1:
                f3 = 0.9
            if tag_id.lower().find("pic") is not -1 or tag_class.lower().find("pic") is not -1:
                f3 = 0.4
            if tag_id.lower().find("content") is not -1 or tag_class.lower().find("content") is not -1:
                f3 = 0.3
            if tag_id.lower().find("text") is not -1 or tag_class.lower().find("text") is not -1:
                f3 = 0.2
            if tag_id.lower().find("author") is not -1 or tag_class.lower().find("author") is not -1:
                f3 = 0.1
            if tag_id.lower().find("editor") is not -1 or tag_class.lower().find("editor") is not -1:
                f3 = 0
        except AttributeError:
            pass

        f4 = row[7] / 100
        if f4 > 1:
            f4 = 1

        content = row[8]
        # f5 = 50
        # try:
        #     if content.find("记者") is not -1:
        #         f5 = 15
        #     if content.find("编辑") is not -1 or content.find("撰文") is not 1:
        #         f5 = 10
        #     if content.find("原标题") is not -1:
        #         f5 = 0
        # except AttributeError:
        #     pass

        print "%d 1:%f 2:%f 3:%f 4:%f \n" % (result, f1, f2, f3, f4)
        txt.write("%d 1:%f 2:%f 3:%f 4:%f \n" % (result, f1, f2, f3, f4))
        show_.write(content + "\n")


def show(id_):
    test = open("/Volumes/mobile/show%d.txt" % id_, "r")
    alltest = test.readlines()
    out = open("/Volumes/mobile/content_test.out", "r")
    allout = out.readlines()

    db = MySQLdb.connect("qisama.me",
                         "root",
                         "smghd",
                         "svm",
                         charset="utf8")
    cursor = db.cursor()
    sql = 'SELECT * FROM content_info_copy WHERE url_id = 1'
    cursor.execute(sql)
    results = cursor.fetchall()

    for i in range(0, len(allout)):
        a = allout[i]
        if a.find('1') is not -1:
            print "标题:" + results[i][8]
        if a.find('2') is not -1:
            print "正文:"+results[i][8]


if __name__ == '__main__':
    exporthtml2txt()
    # exporthtml2txt_out(1)
    # show(1)