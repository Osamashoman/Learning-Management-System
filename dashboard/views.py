from django.shortcuts import render

# Create your views here.
from classroom.models import Course


def home(request):
    c = Course.objects.all()
    name ="Ahmad"
    Pho = 788386675
    print(c)
    context = {"courses": c, "name": name ,"Phone": Pho, }
    return render(request, 'luma/Demos/Fixed_Layout/instructor-courses.html', context)





