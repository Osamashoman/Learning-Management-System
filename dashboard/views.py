import os

import boto3
from django.shortcuts import render, redirect
from camp200.settings import AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET


# Create your views here.
from classroom.models import Course
# Create your views here.
from classroom.models import Course


def home(request):
    c = Course.objects.all()
    name ="Ahmad"
    Pho = 788386675
    print(c)
    context = {"courses": c, "name": name ,"Phone": Pho, }
    return render(request, 'luma/Demos/Fixed_Layout/instructor-courses.html', context)




def home(request):
    return render(request, 'luma/Demos/Fixed_Layout/index.html')



def upload(fileToUpload , x):

    client = boto3.client("s3",
                          aws_access_key_id="AKIA4RTB2YTTOFUBDLMI",
                          aws_secret_access_key="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")


    client.upload_fileobj( fileToUpload , "imgcourses", f"course-{x}.jpg")
    return f"course-{x}.jpg"

def courses(request,course_id=None):
    print(course_id)


    if request.method == 'POST':



        Title = request.POST['Course_title']
        Description = request.POST['Description']
        Video_link = request.POST['Video_link']
        Price = request.POST['price']

        Course.objects.create(title=Title, description=Description, promo_video=Video_link, price=Price)
        course_id = Course.objects.get(title=Title)

        fileToUpload = request.FILES.get('image_file')
        image_key = upload(fileToUpload,course_id.id)

        Course.objects.filter(id=course_id.id).update(image_key=image_key)

        return redirect(courses)
    elif request.method == 'GET':
        context = {}
        if course_id:
            context['course'] = Course.objects.get(id=course_id)
        return render(request, 'luma/Demos/Fixed_Layout/instructor-edit-course.html', context=context)



