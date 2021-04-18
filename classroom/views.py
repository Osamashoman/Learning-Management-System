from django.shortcuts import render
from classroom.models import Lesson, Course, Section
import re


def show_lesson(request, lesson_id=None):
    lesson = Lesson.objects.get(id=lesson_id)
    vimeo_video_id = re.search('(\/)(\d+$)', lesson.link)
    context = {"lesson": lesson, 'vimeo_id': vimeo_video_id.group(2)}
    return render(request, 'luma/Demos/Fixed_Layout/student-take-lesson-layth-edit.html', context)


def show_erolled_courses(request):
    print(request.user.id)
    courses = request.user.studentprofile.courses.all()
    context = {"courses": courses}

    return render(request, 'luma/Demos/Fixed_Layout/student-my-courses.html', context)


def take_course(request, course_id):
    course = Course.objects.get(id=course_id)
    sections = Section.objects.filter(course_id=course_id)
    lessons = Lesson.objects.filter(section__course_id=course_id)

    context = {
        'course': course,
        'sections': sections,
        'lessons': lessons
    }
    return render(request, 'luma/Demos/Fixed_Layout/student-take-course.html', context=context)
