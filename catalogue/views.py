
from catalogue.models import MyUser, StudentProfile

from django.contrib.auth import get_user_model, login, authenticate, logout
from django.core.mail import send_mail
from catalogue.models import MyUser
from django.shortcuts import render, redirect
from classroom.models import *
from dashboard.utilty import VimeoManager



def index(request):
    c = Course.objects.all()
    context = {"courses": c}
    return render(request, 'luma/Demos/Fixed_Layout/index.html', context)


def sections_in_course(request, course_id):

    sections = Section.objects.filter(course_id=course_id)
    course = Course.objects.get(id=course_id)

    vimeo_video_id=VimeoManager.get_id_from_url(None,course.promo_video)
    lessonssum = sum(list(Lesson.objects.all().values_list('duration', flat=True)))

    context = {'sections': sections,
               'course': course,
               'lessonssum': time.gmtime(lessonssum),
               'vimeo_video_id': vimeo_video_id,


               }
    return render(request, 'luma/Demos/Fixed_Layout/student-course.html', context)


def sign_up(request):
    if request.method == 'POST':
        print(request.POST)
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        User = get_user_model()
        user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, password=password)
        login(request, user)
        return redirect(index)
    else:
        return render(request, 'luma/Demos/Fixed_Layout/signup.html')


def sign_in(request):
    context = {}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect(index)
        else:
            context['error'] = True

    return render(request, "luma/Demos/Fixed_Layout/login.html", context)


def sign_out(request):
    logout(request)
    return redirect(index)


def reset_password(request):
    context = {}
    if request.method == 'POST':
        r = request.POST
        email = r['email']
        user = MyUser.objects.get(email=email)
        link = f'http://127.0.0.1:8000/change_password_form/{user.id}/'
        send_mail('reset password', f' this link for rest password {link}  ', 'luma@outlook.com', [email])
        context['Done'] = True
    return render(request, 'luma/Demos/Fixed_Layout/reset-password.html', context)


def change_password_form(request, user_id):
    context = {'user_id': user_id}
    return render(request, 'luma/Demos/Fixed_Layout/change-password.html' ,context)


def change_password(request):
    password = request.POST['password']
    user_id = request.POST['user_id']
    user = MyUser.objects.get(id=user_id)
    user.set_password(password)
    user.save()
    return redirect(sign_in)

def edit_account(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        user = request.user
        user.first_name = firstname
        user.last_name = lastname
        user.save()

    return render(request, 'luma/Demos/Fixed_Layout/edit-account.html')

def buy_course(request,course_id):

    user_id=StudentProfile.objects.get(user_id=request.user.id)
    course=Course.objects.get(id=course_id)
    user_id.courses.add(course)
    return redirect(sections_in_course ,course_id=course_id)

def confirm_buy(request,course_id):

    course = Course.objects.get(id=course_id)

    context = {'price':course.price,
               'title':course.title,
               'course_id':course_id

    }
    return render(request, 'luma/Demos/Fixed_Layout/course enroll.html', context )