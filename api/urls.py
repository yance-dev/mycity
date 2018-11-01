# -*- coding: utf-8 -*-
from django.conf.urls import url,include

from api.views import course,news,account
# from api.views import account


urlpatterns = [
    url(r'^login/$', account.loginView.as_view()),
    url(r'^course/$', course.CourseView.as_view({'get':'list'})),

    url(r'^course/(?P<pk>\d+)/$', course.CourseView.as_view({'get':'retrieve'})),

    url(r'^news/$', news.DeepNews.as_view({"get": "list"})),
    url(r'^news/(?P<pk>\d+)/$', news.DeepNews.as_view({"get": "retrieve"})),

    # url(r'^news/(?P<pk>\d+)/like/$', news..as_view({'post': 'post'})),

]


