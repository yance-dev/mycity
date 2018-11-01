#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 16:27
# @Author  : Young
# @File    : response_dict.py
# @Software: PyCharm
# code,code,code!


class BaseResponse(object):
    """
    封装的返回信息类
    """
    def __init__(self):
        self.code = 1000
        self.data = None
        self.error = None

    @property
    def dict(self):
        return self.__dict__
