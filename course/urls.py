from django.urls import path
from course import views

urlpatterns = [
    path('lesson/<int:lesson_id>/lesson/user/create/', views.LessonUserCreateAPIView.as_view()),
    path('course/<int:pk>/', views.CourseDetailAPIView.as_view()),
]