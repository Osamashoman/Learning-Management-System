from dashboard import views
from django.urls import path

urlpatterns = [
    path('Homepage', views.home),
    path('courses', views.courses, name='courses'),
    path('courses/<int:course_id>/', views.courses)
]
