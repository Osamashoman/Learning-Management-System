from django.shortcuts import render
from classroom.models import Lesson
import re


def show_lesson(request, lesson_id=None):
    lesson = Lesson.objects.get(id=lesson_id)
    vimeo_video_id = re.search('(\/)(\d+$)', lesson.link)
    context = {"lesson": lesson, 'vimeo_id': vimeo_video_id.group(2)}
    return render(request, 'luma/Demos/Fixed_Layout/student-take-lesson-layth-edit.html', context)


