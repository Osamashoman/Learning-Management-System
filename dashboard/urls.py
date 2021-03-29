from django.urls import path

from dashboard import views

urlpatterns = [
    path('Homepage', views.home),
    path('courses', views.courses, name='courses'),
    path('courses/<int:course_id>/', views.courses, name='update-course'),
    path('bill', views.index),

]
