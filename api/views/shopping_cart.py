#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author    : Young
@Email     : hyc554@outlook.com
@site      : http://www.cnblogs.com/huang-yc/
@File      : shopping_cart.py
@version   : 1.0
@Time      : 2018/11/4 20:51
Description about this file: 

"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSetMixin
from django_redis import get_redis_connection
from utils.response_dict import BaseResponse
from api.views.auth import YcAuth
from api import models
from utils.error import PricePolicyInvalid
from django.core.exceptions import ObjectDoesNotExist


class ShoppingCart(ViewSetMixin, APIView):
    authentication_classes = [YcAuth]
    conn = get_redis_connection('default')
    ret = BaseResponse()

    def create(self, request, *args, **kwargs):
        try:
            # 在这里获得用户的课程ID与价格策略ID
            course_id = int(request.data.get('course_id'))
            policy_id = int(request.data.get('policy_id'))

            # 2. 获取专题课信息
            course = models.Course.objects.get(id=course_id)

            # 3.获取课程相关的所有价格策略
            price_policy_list = course.price_policy.all()
            price_policy_dict = {}
            for item in price_policy_list:
                price_policy_dict[item.id] = {
                    "period": item.valid_period,
                    "period_display": item.get_valid_period_display(),
                    "price": item.price
                }
            # print(price_policy_dict)
            if policy_id not in price_policy_dict:
                raise PricePolicyInvalid('价格策略不合法')


        except PricePolicyInvalid as e:
            self.ret.data = 2001
            self.ret.error = e.msg
        except ObjectDoesNotExist as e:
            self.ret.data = 2002
            self.ret.error = '课程不存在'


        except Exception as e:
            self.ret.code = 1001
            self.ret.data = '获取购物车数据失败'
        return Response(self.ret.dict)
