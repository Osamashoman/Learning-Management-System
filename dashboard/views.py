import re
import time

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from classroom.models import Course, Lesson
from dashboard.utilty import S3Manager, VimeoManager


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
    context = {"courses": courses}
    return render(request, 'luma/Demos/Fixed_Layout/instructor-courses.html', context)


def course_crud(request, course_id=None):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')

        Title = request.POST['Course_title']
        Description = request.POST['Description']
        Video_link = request.POST['Video_link']
        Price = request.POST['price']
        fileToUpload = request.FILES.get('image_file')
        if course_id:
            image_key = str(course_id) + '.jpg'

            course = Course.objects.filter(id=course_id).update(title=Title, description=Description,
                                                                promo_video=Video_link, price=Price)

            if request.FILES.get('image_file'):
                s3 = S3Manager()
                s3.upload(fileToUpload, settings.COURSES_IMAGES_BUCKET, image_key)

            return redirect(course_crud, course_id=course_id)

        else:
            s3 = S3Manager()
            course = Course.objects.create(title=Title, description=Description, promo_video=Video_link, price=Price)

            image_key = str(course.id) + '.jpg'
            s3.upload(fileToUpload, settings.COURSES_IMAGES_BUCKET, image_key)

            Course.objects.filter(id=course.id).update(image_key=image_key)
            return redirect(course_crud, course_id=course.id)
    elif request.method == 'GET':
        context = {}
        if course_id:
            context['course'] = Course.objects.get(id=course_id)
        return render(request, 'luma/Demos/Fixed_Layout/instructor-edit-course.html', context=context)


def course_view(request, course_id=None):
    # Show course View
    # Get course from database
    course = Course.objects.get(id=course_id)
    vimeo_video_id = re.search('(\/)(\d+$)', course.promo_video)
    context = {"course": course, 'vimeo_id': vimeo_video_id.group(2)}
    print(context)
    return render(request, 'luma/Demos/Fixed_Layout/dashboard-show-course.html', context)



