# coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Result(models.Model):
    """保存识别结果"""
    status_code = models.IntegerField(3)
    title = models.CharField(max_length=255)
    content = models.TextField()
    url = models.URLField()
