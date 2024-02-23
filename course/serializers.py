from rest_framework import serializers
from course import models


class LessonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LessonUser
        fields = (
            'is_completed',
            'watched_time',
        )


class LessonSerializer(serializers.ModelSerializer):
    watched_time = serializers.IntegerField()
    is_completed = serializers.BooleanField()
    last_viewed = serializers.DateTimeField()

    # lesson_user = serializers.SerializerMethodField()

    class Meta:
        model = models.Lesson
        fields = (
            'id',
            'title',
            'video',
            'total_time',
            'watched_time',
            'is_completed',
            'last_viewed',
            # 'lesson_user'
        )

    def get_lesson_user(self, obj):
        stmt = models.LessonUser.objects.filter(user=self.context['request'].user, lesson=obj.id).first()
        serializer = LessonUserSerializer(stmt)
        return serializer.data


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


class CourseStatisticSerializer(serializers.ModelSerializer):
    views = serializers.IntegerField()
    watched_time_in_seconds = serializers.IntegerField()
    current_students_count = serializers.IntegerField()
    users_bought = serializers.IntegerField()
    percentage_of_buying = serializers.FloatField()

    class Meta:
        model = models.Course
        fields = (
            'id',
            'title',
            'views',
            'watched_time_in_seconds',
            'current_students_count',
            'users_bought',
            'percentage_of_buying',
        )
