import re
import time

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from classroom.models import Course, Lesson
from dashboard.utilty import S3Manager, VimeoManager, S3ObjectsFormatters


def lesson(request, section_id, lesson_id=None):
    context = {"section_id": section_id, "lesson_id": lesson_id}
    if lesson_id:
        lesson = Lesson.objects.get(id=lesson_id)
        context['duration'] = time.gmtime(lesson.duration)
        context['lesson_obj'] = lesson

    return render(request, 'luma/Demos/Fixed_Layout/create_lesson.html', context)


def create_or_update_lesson(request):
    lesson_id = request.POST.get('lesson_id')
    defaults = {'title': request.POST["title"],
                'type': request.POST["type"],
                'link': request.POST['link'],
                'section_id': request.POST['section_id']}

    if request.POST['type'] == 'Uploaded Video':
        defaults['duration'] = VimeoManager().get_vimeo_duration(request.POST['link'])

    Lesson.objects.update_or_create(id=lesson_id, defaults=defaults)

    messages.add_message(request, messages.INFO, '')
    return redirect('lesson', section_id=request.POST['section_id'])


def courses(request):
    courses = Course.objects.all()
    context = {"courses": courses, 'BUCKET': settings.COURSES_IMAGES_BUCKET}
    return render(request, 'luma/Demos/Fixed_Layout/instructor-courses.html', context)


def course_crud(request, course_id=None):
    course_id = request.POST.get('course_id')
    fileToUpload = request.FILES.get('image_file')
    #
    defaults = {'title': request.POST["Course_title"],
                'description': request.POST["Description"],
                'promo_video': request.POST['Video_link'],
                'price': request.POST['price']
                }

    course, created = Course.objects.update_or_create(id=course_id, defaults=defaults)

    if fileToUpload:
        s3 = S3Manager()
        # image_key = 'course' + str(course.id) + '.jpg'
        image_key = S3ObjectsFormatters.course_image(course_id)
        s3.upload(fileToUpload, settings.COURSES_IMAGES_BUCKET, image_key)
        course.image_key = image_key
        course.save()

    return redirect(course_form, course_id=course.id)


def course_form(request, course_id=None):
    context = {}
    if course_id:
        course = Course.objects.get(id=course_id)
        re_result = re.search('(.com\/)([\d]+)', course.promo_video)
        print(re_result)
        context = {'course': Course.objects.get(id=course_id), 'vimeo_id': re_result.group(2),
                   'image_key': course.image_key, 'BUCKET': settings.COURSES_IMAGES_BUCKET}
    return render(request, 'luma/Demos/Fixed_Layout/instructor-edit-course.html', context=context)


def course_view(request, course_id=None):
    # Show course View
    # Get course from database
    course = Course.objects.get(id=course_id)
    vimeo_video_id = re.search('(\/)(\d+$)', course.promo_video)
    context = {"course": course, 'vimeo_id': vimeo_video_id.group(2)}
    return render(request, 'luma/Demos/Fixed_Layout/dashboard-show-course.html', context)


def delete_course(request, course_id):
    image_key = S3ObjectsFormatters.course_image(course_id)
    S3Manager().delete(settings.COURSES_IMAGES_BUCKET, image_key)
    Course.objects.get(id=course_id).delete()
    return redirect('show-courses')
