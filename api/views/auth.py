#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 16:50
# @Author  : Young
# @Email   : hyc554@outlook.com
# @File    : auth.py


from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from api import models


class YcAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        obj = models.UserAuthToken.objects.filter(token=token).first()
        if not obj:
            raise exceptions.AuthenticationFailed('认证失败')
        return (obj.user.username, obj)

