import time

from django.shortcuts import render
from classroom.models import Lesson, Course

import re


def show_lesson(request, lesson_id=None):
    lesson = Lesson.objects.get(id=lesson_id)
    vimeo_video_id = re.search('(\/)(\d+$)', lesson.link)
    context = {"lesson": lesson, 'vimeo_id': vimeo_video_id.group(2)}
    return render(request, 'luma/Demos/Fixed_Layout/student-take-lesson-layth-edit.html', context)


def show_erolled_courses(request):
    print(request.user.id)
    courses = request.user.StudentProfile.courses.all()
    numlesson = Course.num_lessons
    lessonssum = sum(list(Lesson.objects.all().exclude(duration=None).values_list('duration', flat=True)))
    context = {"courses": courses,
               'numlesson': numlesson,
               'lessonssum': time.gmtime(lessonssum)}

    return render(request, 'luma/Demos/Fixed_Layout/student-my-courses.html', context)
