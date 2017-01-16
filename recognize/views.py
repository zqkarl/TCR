# encoding: utf-8

# Create your views here.
import json
import requests
import models
from django.http import HttpResponse
from svmutil import *
import logging
from services import HtmlPurify
from services import Recognize
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)


def recognize(request):
    url = request.GET['url']  # 需要识别的网址
    out = {'code': 200}
    try:
        soup = HtmlPurify.purify(url)
        result = Recognize.traversal(soup)
        out['result'] = result
    # except (requests.ConnectionError, requests.MaxRetryError) as e:
    #     out['code'] = 404
    #     out['error'] = e.message
    except Exception, e:
        out['code'] = 500
        out['error'] = e.message
    finally:
        r = models.Result(url=url)
        r.status_code = out.get('code')
        if out.get('result') is not None:
            r.title = out.get('result').get('title')
            r.content = out.get('result').get('content')
        else:
            r.title = out.get('error')
            r.content = out.get('error')
        r.save()
    python_to_json = json.dumps(out, ensure_ascii=False)
    return HttpResponse(python_to_json)
