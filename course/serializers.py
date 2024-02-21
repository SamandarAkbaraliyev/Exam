from rest_framework import serializers
from course import models


class LessonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LessonUser
        fields = (
            'has_access',
            'is_completed',
            'watched_time',
        )


class LessonSerializer(serializers.ModelSerializer):
    lesson_user = LessonUserSerializer()

    class Meta:
        model = models.Lesson
        fields = (
            'id',
            'title',
            'video',
            'total_time',
            'lesson_user',
        )


class CourseSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    lessons = LessonSerializer(many=True)

    class Meta:
        model = models.Course
        fields = (
            'id',
            'author',
            'title',
            'description',
            'lessons',
        )


class LessonUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LessonUser
        fields = (
            'user',
            'lesson',
        )
