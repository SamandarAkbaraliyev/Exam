from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from moviepy.editor import VideoFileClip


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(BaseModel):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='author')
    is_bought = models.ManyToManyField(get_user_model(), related_name='buyers', blank=True)
    title = models.CharField(max_length=256)
    description = models.TextField()

    def __str__(self):
        return self.title


class Lesson(BaseModel):
    course = models.ManyToManyField(Course, related_name='lessons')
    title = models.CharField(max_length=256)
    video = models.FileField(upload_to='lessons/')
    order = models.PositiveIntegerField(default=0)
    total_time = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return self.title


class LessonUser(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='lesson_user')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_user')
    has_access = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    watched_time = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user}\' {self.lesson}'


class LessonUserWatched(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='lesson_user_watched')
    lesson_user = models.ForeignKey(LessonUser, on_delete=models.CASCADE, related_name='lesson_user_watched')
    from_time = models.PositiveIntegerField(default=0)
    to_time = models.PositiveIntegerField(default=0)


@receiver(post_save, sender=Lesson)
def calculate_video_length(sender, instance, created, **kwargs):
    if created:
        video = VideoFileClip(instance.video.path)
        instance.total_time = video.duration
        instance.save()
