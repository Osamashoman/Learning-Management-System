from django.shortcuts import render
from classroom.models import Course


def index(request):
	c = Course.objects.all()
	context = {"courses": c}
	return render(request, 'luma/Demos/Fixed_Layout/index.html', context)
