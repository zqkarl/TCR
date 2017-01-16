# coding=utf8
import bs4
import requests
import logging
import datetime
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')

logger = logging.getLogger(__name__)


def purify(url):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }
    r = requests.get(url, headers=header)
    logger.info('开始请求%s，返回状态码为%d,当前时间为%s' % (url, r.status_code, datetime.datetime.now()))

    # 如果请求失败重试三次
    if r.status_code != 200:
        i = 0
        while i < 3 and r.status_code != 200:
            logger.info('正在重试第%d次'%i+1)
            r = requests.get(url, headers=header)
            i += 1
        if r.status_code != 200:
            raise requests.ConnectionError('网址连接失败')

    content = r.text

    # 编码判断(待改进)
    try:
        content = content.encode(r.encoding).decode("utf8")
    except UnicodeDecodeError:
        content = content.encode(r.encoding).decode("GB18030")
    except UnicodeEncodeError:
        content = content.encode("GB18030").decode("GB18030")

    logger.debug("网址%s \n"
                 "编码%s \n"
                 "返回内容%s \n"
                 % (url, r.encoding, content))

    soup = BeautifulSoup(content, "lxml")

    try:
        for script in soup.find_all('script'):
            script.decompose()
    except TypeError:
        pass
    try:
        for style in soup.find_all('style'):
            style.decompose()
    except TypeError:
        pass
    try:
        for meta in soup.find_all('meta'):
            meta.decompose()
    except TypeError:
        pass
    try:
        for form in soup.find_all('soup'):
            form.decompose()
    except TypeError:
        pass
    try:
        for inputs in soup.find_all('input'):
            inputs.decompose()
    except TypeError:
        pass
    try:
        for select in soup.find_all('select'):
            select.decompse()
    except TypeError:
        pass
    try:
        for link in soup.find_all('link'):
            link.decompse()
    except TypeError:
        pass

    # print soup.prettify()

    return soup

if __name__ == '__main__':
    purify("http://app1.sfda.gov.cn/datasearch/schedule/search.jsp?tableId=43&tableName=TABLE43&columnName=COLUMN464,COLUMN475&title1=%E8%8D%AF%E5%93%81")