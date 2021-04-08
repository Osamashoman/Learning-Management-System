from django.urls import path

from catalogue import views

urlpatterns = [
    path("", views.index),
    path('signup/', views.sign_up, name='sign_up'),
    path('signin/', views.sign_in),
    path('signout/', views.sign_out),
    path('reset_password/', views.reset_password),
    path('change_password_form/<int:user_id>/', views.change_password_form),
    path('change_password/', views.change_password)
]
