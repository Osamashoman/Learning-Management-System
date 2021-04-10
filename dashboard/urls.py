from django.urls import path
from dashboard import views

urlpatterns = [
    path('lesson/<int:section_id>/', views.lesson, name='lesson'),
    path('lesson/<int:section_id>/<int:lesson_id>/', views.lesson, name='update-lesson'),
    path('lesson/create_or_update/', views.create_or_update_lesson, name='create-lesson'),
    path('courses/', views.courses ,name= 'show-courses'),
    path('course/create/', views.course_form, name='create-course-form'),
    path('course/update/<int:course_id>/', views.course_form, name='update-course-form'),
    path('course/create_or_update/', views.course_crud, name='create-or-update'),
    path('course/view/<int:course_id>/', views.course_view, name='view_course'),
    path('course/delete/<int:course_id>/', views.delete_course, name='delete-course'),
    path('section/<int:course_id>/<int:section_id>/', views.create_section, name='create-section'),
    path('section/<int:course_id>/', views.create_section, name='create-section'),
    path('section/create_or_update_section/', views.create_or_update_section, name='create_or_update_section')
]
