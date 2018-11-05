# -*- coding: utf-8 -*-
from django.conf.urls import url,include

from api.views import course,news,account,shopping_cart
# from api.views import account
from api import tests

urlpatterns = [
    url(r'^login/$', account.loginView.as_view()),
    url(r'^course/$', course.CourseView.as_view({'get':'list'})),

    url(r'^course/(?P<pk>\d+)/$', course.CourseView.as_view({'get':'retrieve'})),

    url(r'^news/$', news.DeepNews.as_view({"get": "list"})),
    url(r'^news/$', news.DeepNews.as_view({"get": "list"})),
    url(r'^shopping_cart/$', shopping_cart.ShoppingCart.as_view({"post": "create"})),

    # url(r'^news/(?P<pk>\d+)/like/$', news..as_view({'post': 'post'})),
    url(r'^index/$',tests.Index.as_view()),
]


