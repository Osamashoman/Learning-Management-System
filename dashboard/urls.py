from django.urls import path

from dashboard import views

urlpatterns = [
    path('lesson/<int:section_id>/', views.lesson, name='lesson'),
    path('lesson/<int:section_id>/<int:lesson_id>/', views.lesson, name='update-lesson'),
    path('lesson/create_or_update/', views.create_or_update_lesson, name='create-lesson'),
    path('courses/', views.courses),
    path('course/create/', views.course_crud, name='create-course'),
    path('course/update/<int:course_id>/', views.course_crud, name='update-course'),
    path('course/view/<int:course_id>/', views.course_view)
]
