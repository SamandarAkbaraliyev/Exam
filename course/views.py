from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from course import models
from course import serializers
from course.permissions import IsBuyer
from django.db.models import Prefetch, Subquery, OuterRef, Sum, Count, Case, When, F
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User


class LessonUserCreateAPIView(generics.CreateAPIView):
    queryset = models.LessonUser.objects.all()
    serializer_class = serializers.LessonUserCreateSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        lesson_id = self.kwargs.get('lesson_id')
        lesson = models.Lesson.objects.get(id=lesson_id)
        lesson_user = models.LessonUser.objects.create(user=user, lesson=lesson)
        data = serializers.LessonUserCreateSerializer(lesson_user)
        return Response({'data': data})


class CourseListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer

    def get_queryset(self):
        user = self.request.user
        query = models.LessonUser.objects.filter(user=user, lesson=OuterRef('pk'))
        sq_watched_time = Subquery(query.values('watched_time'))
        sq_is_completed = Subquery(query.values('is_completed'))
        prefetch = Prefetch('lessons',
                            models.Lesson.objects.annotate(watched_time=sq_watched_time, is_completed=sq_is_completed))
        qs = super().get_queryset().prefetch_related(prefetch, 'lessons', 'is_bought').select_related('author') \
            .filter(is_bought=user)

        return qs


class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        query = models.LessonUser.objects.filter(user=user, lesson=OuterRef('pk'))
        sq_watched_time = Subquery(query.values('watched_time'))
        sq_is_completed = Subquery(query.values('is_completed'))
        sq_modified_at = Subquery(query.values('last_viewed'))
        prefetch = Prefetch('lessons',
                            models.Lesson.objects.annotate(watched_time=sq_watched_time, is_completed=sq_is_completed,
                                                           last_viewed=sq_modified_at))
        qs = super().get_queryset().prefetch_related(prefetch, 'lessons', 'is_bought').select_related('author') \
            .filter(is_bought=user)

        return qs


class CourseStatisticsAPIView(generics.ListAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseStatisticSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        users_count = User.objects.count()

        qs = super().get_queryset().annotate(
            views=Coalesce(Sum('lessons__views'), 0),
            watched_time_in_seconds=Coalesce(
                Sum('lessons__lesson_user__watched_time'), 0),
            current_students_count=Coalesce(
                Sum(Case(When(lessons__lesson_user__is_completed=False, then=1),
                         When(lessons__lesson_user__is_completed=True, then=0))), 0),
            users_bought=Count('is_bought', distinct=True),
            percentage_of_buying=(F('users_bought') * 100 / users_count)
        )
        return qs
