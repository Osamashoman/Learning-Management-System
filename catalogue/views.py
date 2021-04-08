from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect

from catalogue.models import MyUser
from classroom.models import Course
from django.contrib.auth import authenticate, login, get_user_model, logout


def index(request):
    c = Course.objects.all()
    context = {"courses": c}
    return render(request, 'luma/Demos/Fixed_Layout/index.html', context)


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
