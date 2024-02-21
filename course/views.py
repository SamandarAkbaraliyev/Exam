from rest_framework import generics
from rest_framework.response import Response
from course import models
from course import serializers
from course.permissions import IsBuyer



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


class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = models.Course.objects.all().prefetch_related('lessons')
    serializer_class = serializers.CourseSerializer
    permission_classes = (IsBuyer, )

