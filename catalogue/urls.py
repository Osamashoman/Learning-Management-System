from django.urls import path

from catalogue import views

urlpatterns = [
	path("", views.index)
]