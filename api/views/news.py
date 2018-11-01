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


class DeepNews(ViewSetMixin, APIView):
    authentication_classes = [YcAuth,]

    def list(self, request, *args, **kwargs):
        """
        推文列表内容
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ret = BaseResponse()
        try:
            article_list = models.Article.objects.all()
            serialized_art_list = ArticleSerializers(instance=article_list, many=True)
            ret.data = serialized_art_list.data
        except Exception as e:
            ret.code = 1001
            ret.error = '未获取到资源'
        return Response(ret.dict)

    def retrieve(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            pk = kwargs.get('pk')
            obj = models.Article.objects.filter(pk=pk).first()
            ser = ArticleDetailSerializers(instance=obj, many=False)
            ret.data = ser.data
        except Exception as e:
            ret.data = 1001
            ret.error = '未获取到资源'
        return Response(ret.dict)
