from django.urls import path

from catalogue import views

urlpatterns = [
    path("", views.index),
    path("course_catalogue/<int:course_id>/", views.sections_in_course, name="sections-in-course")

]
