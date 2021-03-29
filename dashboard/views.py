from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

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
