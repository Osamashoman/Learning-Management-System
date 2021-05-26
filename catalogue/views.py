import datetime

from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.views import View

from camp200.settings import EMAIL_HOST_USER
from catalogue.models import MyUser, StudentProfile, UserResetCode
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.core.mail import send_mail
from catalogue.models import MyUser
from django.shortcuts import render, redirect
from classroom.models import *
from dashboard.utilty import VimeoManager
from django.utils.crypto import get_random_string
from django.views import View


class SignUpView(View):
    template = 'luma/Demos/Fixed_Layout/signup.html'

    def post(self, request):
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        User = get_user_model()
        user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email,
                                        password=password)
        StudentProfile.objects.create(user=user)
        login(request, user)
        return redirect(index)

    def get(self, request):
        return render(request, self.template)


def index(request):
    c = Course.objects.all()
    context = {"courses": c}
    return render(request, 'luma/Demos/Fixed_Layout/index.html', context)


def course(request, course_id):
    sections = Section.objects.filter(course_id=course_id)
    course = Course.objects.get(id=course_id)
    courses = Course.objects.all()

    vimeo_video_id = VimeoManager().get_id_from_url(course.promo_video)
    lessonssum = sum(list(
        Lesson.objects.filter(section__course_id=course_id).exclude(duration=None).values_list('duration', flat=True)))
    if request.user.is_authenticated:
        course_is_enrolled = request.user.studentprofile.courses.filter(id=course_id).exists()
    else:
        course_is_enrolled = False

    context = {'sections': sections,
               'course': course,
               'lessonssum': time.gmtime(lessonssum),
               'vimeo_video_id': vimeo_video_id,
               'courses': courses,
               'course_is_enrolled': course_is_enrolled
               }
    return render(request, 'luma/Demos/Fixed_Layout/student-course.html', context)


class SignInView(View):
    context = {'error':False}
    template = "luma/Demos/Fixed_Layout/login.html"

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        temp=0
        if user:
            login(request, user)
            return redirect(index)
        else:
            self.context['error'] = True

        return render(request, self.template, self.context)

    def get(self, request):
        self.context['error'] = True
        return render(request, self.template, self.context)


def sign_out(request):
    logout(request)
    return redirect(index)


class RestPassword(View):
    def post(self, request):
        context = {}
        r = request.POST
        email = r['email']
        password_reset_code = get_random_string(length=7)

        user = MyUser.objects.get(email=email)
        now = timezone.now()
        time_part_3_minute = datetime.timedelta(seconds=settings.EXPIRATION_PERIOD)
        total = time_part_3_minute + now

        UserResetCode.objects.create(random_code=password_reset_code, user_id=user.id, expiration=total)
        link = f'http://127.0.0.1:8000/change_password_form/{user.id}/{password_reset_code}'
        send_mail('reset password', f' this link for rest password {link}  ', f'{EMAIL_HOST_USER}', [email])
        context['Done'] = True

        return render(request, 'luma/Demos/Fixed_Layout/reset-password.html', context)

    def get(self, request):
        return render(request, 'luma/Demos/Fixed_Layout/reset-password.html')


def change_password_form(request, user_id, password_reset_code):
    context = {}
    check = UserResetCode.objects.get(user_id=user_id, random_code=password_reset_code)
    now = timezone.now()
    context['invalid_link'] = True
    if now > check.expiration or check.check_link:
        return render(request, 'luma/Demos/Fixed_Layout/reset-password.html', context)
    else:
        context = {'user_id': user_id, 'password_reset_code': password_reset_code}
        return render(request, 'luma/Demos/Fixed_Layout/change-password.html', context)


def change_password(request):
    password = request.POST['password']
    user_id = request.POST['user_id']
    password_reset_code = request.POST['password_reset_code']
    user = MyUser.objects.get(id=user_id)
    user.set_password(password)
    user.save()

    password_reset_code = UserResetCode.objects.get(user_id=user_id, random_code=password_reset_code)
    password_reset_code.check_link = True
    password_reset_code.save()
    return redirect('sign_in')


def editAccount(request):
    template = 'luma/Demos/Fixed_Layout/edit-account.html'
    User = request.user
    context = {
        'user': User,
    }
    return render(request, template, context)


def EditAccountView(request):
    template = 'luma/Demos/Fixed_Layout/edit-account.html'

    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    user = request.user
    user.first_name = firstname
    user.last_name = lastname
    user.save()

    return render(request, template)


def buy_course(request, course_id):
    user_id = StudentProfile.objects.get(user_id=request.user.id)
    user_id.courses.add(Course.objects.get(id=course_id))
    return redirect(course, course_id=course_id)


def confirm_buy(request, course_id):
    course = Course.objects.get(id=course_id)

    context = {'price': course.price,
               'title': course.title,
               'course_id': course_id

               }
    return render(request, 'luma/Demos/Fixed_Layout/course enroll.html', context)
