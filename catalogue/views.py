import re
import time

from classroom.models import Lesson
from django.shortcuts import render
from classroom.models import *
from dashboard.utilty import VimeoManager


def index(request):
    c = Course.objects.all()
    context = {"courses": c}
    return render(request, 'luma/Demos/Fixed_Layout/index.html', context)


def sections_in_course(request, course_id):

    sections = Section.objects.filter(course_id=course_id)
    course = Course.objects.get(id=course_id)

    vimeo_video_id=VimeoManager.get_id_from_url(None,course.promo_video)
    lessonssum = sum(list(Lesson.objects.all().values_list('duration', flat=True)))

    context = {'sections': sections,
               'course': course,
               'lessonssum': time.gmtime(lessonssum),
               'vimeo_video_id': vimeo_video_id,


               }
    return render(request, 'luma/Demos/Fixed_Layout/student-course.html', context)
