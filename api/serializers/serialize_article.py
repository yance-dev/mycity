#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author    : Young
@Email     : hyc554@outlook.com
@site      : http://www.cnblogs.com/huang-yc/
@File      : serialize_article.py
@version   : 1.0
@Time      : 2018/11/1 17:21
Description about this file: 

"""
from rest_framework import serializers
from api.models import Article


class ArticleSerializers(serializers.ModelSerializer):
    """
    Article表的序列化
    """
    source = serializers.CharField(source="source.name")
    article_type = serializers.CharField(source="get_article_type_display")
    position = serializers.CharField(source='get_position_display')

    class Meta:
        model = Article
        fields = ["title", "source", "article_type", 'head_img', 'brief', 'pub_date', 'comment_num', 'agree_num',
                  'view_num', 'collect_num', 'position']


class ArticleDetailSerializers(serializers.ModelSerializer):
    """
    ArticleDetail表的序列化
    """
    class Meta:
        model = Article
        fields = ['title', 'pub_date', 'agree_num', 'view_num', 'collect_num', 'comment_num', 'source', 'content',
                  'head_img']
