from django.shortcuts import render

# Create your views here.

def home(request):
	return render(request, 'luma/Demos/Fixed_Layout/index.html')