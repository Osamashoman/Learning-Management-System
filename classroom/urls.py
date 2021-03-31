from django.urls import path
from classroom import views

urlpatterns = [path('lesson/show/<int:lesson_id>', views.show_lesson, name='show_lesson'), ]
