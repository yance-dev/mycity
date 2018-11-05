from django.test import TestCase

# Create your tests here.
import redis
from django.shortcuts import render,HttpResponse
from django_redis import get_redis_connection

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author    : Young
@Email     : hyc554@outlook.com
@site      : http://www.cnblogs.com/huang-yc/
@File      : news.py
@version   : 1.0
@Time      : 2018/11/1 17:06
Description about this file: 

"""
from api import models
from utils.response_dict import BaseResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSetMixin
from api.serializers.serialize_article import ArticleSerializers, ArticleDetailSerializers
from api.views.auth import YcAuth


class Index(APIView):

    def get(self, request, *args, **kwargs):
        conn = get_redis_connection("default")

        return HttpResponse('设置成功')







# def index(request):
#
# def order(request):
#     conn = get_redis_connection("back")
#     return HttpResponse('获取成功')