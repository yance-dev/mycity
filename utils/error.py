#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author    : Young
@Email     : hyc554@outlook.com
@site      : http://www.cnblogs.com/huang-yc/
@File      : error.py
@version   : 1.0
@Time      : 2018/11/5 16:37
Description about this file: 

"""

class PricePolicyInvalid(Exception):
    def __init__(self,msg):
        self.msg = msg


