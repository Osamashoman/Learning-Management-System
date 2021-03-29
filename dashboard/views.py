

import boto3
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import boto3
from classroom.models import Course, Lesson


def lesson_form(request, section_id, lesson_id=None):
    context = {"section_id": section_id, "lesson_id": lesson_id}
    if lesson_id:
        context['lesson_obj'] = Lesson.objects.get(id=lesson_id)

    return render(request, 'luma/Demos/Fixed_Layout/create_lesson.html', context)


@csrf_exempt
def create_lesson(request):
    type = request.POST["ltype"]
    link = request.POST['link']
    title = request.POST["title"]
    lesson_id = request.POST.get('lesson_id')
    # get or createa
    if lesson_id:
        Lesson.objects.filter(id=lesson_id).update(type=type, title=title, link=link, duration=0,
                                                          section_id=request.POST['section_id'])
    else:
        Lesson.objects.create(type=type, title=title, link=link, duration=0, section_id=request.POST['section_id'])

    messages.add_message(request, messages.INFO, 'Hello world.')

    return redirect('lesson', section_id=request.POST['section_id'])


def home(request):
    c = Course.objects.all()
    name = "Ahmad"
    Pho = 788386675

    context = {"courses": c, "name": name, "Phone": Pho, }
    return render(request, 'luma/Demos/Fixed_Layout/instructor-courses.html', context)


def index(request):
    c = Course.objects.all()
    context =  {"courses": c}
    return render(request, 'luma/Demos/Fixed_Layout/index.html', context)


def upload(fileToUpload , x):

    client = boto3.client("s3",
                          aws_access_key_id="AKIA4RTB2YTTOFUBDLMI",
                          aws_secret_access_key="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")


    client.upload_fileobj( fileToUpload , "imgcourses", f"course-{x}.jpg")
    return f"course-{x}.jpg"

def courses(request,course_id=None):



    if request.method == 'POST':
        course_id = request.POST.get('course_id')

        Title = request.POST['Course_title']
        Description = request.POST['Description']
        Video_link = request.POST['Video_link']
        Price = request.POST['price']
        fileToUpload = request.FILES.get('image_file')
        if course_id :
            course= Course.objects.filter(id=course_id).update(title=Title, description=Description, promo_video=Video_link, price=Price)

            if request.FILES.get('image_file'):
                image_key = upload(fileToUpload, course_id)


        else:
            course = Course.objects.create(title=Title, description=Description, promo_video=Video_link, price=Price)

            image_key = upload(fileToUpload, course.id)

            Course.objects.filter(id=course_id.id).update(image_key=image_key)

        return redirect(courses ,course_id=course_id)
    elif request.method == 'GET':
        context = {}
        if course_id:
            context['course'] = Course.objects.get(id=course_id)
        return render(request, 'luma/Demos/Fixed_Layout/instructor-edit-course.html', context=context)

