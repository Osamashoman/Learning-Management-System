from django.urls import path

from dashboard import views

urlpatterns = [
    path('lessons/<int:section_id>/', views.lesson_form, name='lesson'),
    path('lessons/<int:section_id>/<int:lesson_id>/', views.lesson_form, name='update_lesson'),
    path('create_lesson', views.create_lesson, name='createlesson'),
    path('Homepage', views.home),
    path('courses', views.courses, name='courses'),
    path('courses/<int:course_id>/', views.courses, name='update-course'),
    path('bill', views.index),

]
