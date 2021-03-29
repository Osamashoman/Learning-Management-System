from django.urls import path

from dashboard import views

urlpatterns = [
    path('<int:section_id>', views.lesson_form, name='lesson'),
    path('<int:section_id>/<int:lesson_id>', views.lesson_form, name='update_lesson'),
    path('create_lesson', views.create_lesson, name='createlesson'),


]
