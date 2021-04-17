import time
from itertools import count

from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    promo_video = models.CharField(max_length=200)
    image_key = models.CharField(max_length=200, blank=True)
    price = models.FloatField()

    @property
    def num_lessons(self):
        sections = self.section_set.all()
        num_lessons = Lesson.objects.filter(section__in=sections).count()
        return num_lessons

    @property
    def duration(self):
        duration_seconds=  sum(list(Lesson.objects.filter(section__course_id=self.id).exclude(duration=None).values_list('duration', flat=True)))
        time_obj = time.gmtime(duration_seconds)
        hours = time_obj.tm_hour
        minutes = time_obj.tm_min
        seconds = time_obj.tm_sec
        return hours, minutes, seconds


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)


class Lesson(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    duration = models.IntegerField(null=True)
    free_sample = models.BooleanField(default=False)

    @property
    def duration_gmtime_object(self):
        return time.gmtime(self.duration)
