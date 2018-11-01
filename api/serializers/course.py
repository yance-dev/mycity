# -*- coding: utf-8 -*-
from rest_framework import serializers
from api import models


class CourseSerializer(serializers.ModelSerializer):
    """
    Course的序列化
    """

    class Meta:
        model = models.Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    """
    CourseDetail序列化
    """
    # # one2one/fk/choice
    title = serializers.CharField(source='course.name')
    img = serializers.CharField(source='course.course_img')
    level = serializers.CharField(source='course.get_level_display')
    #
    # m2m
    recommends = serializers.SerializerMethodField()
    chapter = serializers.SerializerMethodField()
    teachers = serializers.SerializerMethodField()

    class Meta:
        model = models.CourseDetail
        fields = ['hours', 'why_study', 'title', 'img', 'course', 'course_slogan','level', 'recommends', 'chapter','teachers']
        # fields ='__all__'
    def get_recommends(self, obj):
        # 获取推荐的所有课程
        print('1')
        queryset = obj.recommend_courses.all()

        return [{'id': row.id, 'name': row.name} for row in queryset]

    def get_chapter(self, obj):
        # 获取课程对应章节
        print('2')

        queryset = obj.course.coursechapters.all()

        return [{'id': row.id, 'name': row.name} for row in queryset]

    def get_teachers(self, obj):
        # 获取课程负责的老师
        print('3')

        queryset = obj.teachers.all()

        return [{'id': row.id, 'name': row.name} for row in queryset]

