

import boto3
from django.shortcuts import render, redirect



# Create your views here.
from classroom.models import Course


def home(request):
    return render(request, 'luma/Demos/Fixed_Layout/index.html')



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
                image_key = upload(fileToUpload, course_id.id)


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



