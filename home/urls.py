from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('generic-student/', StudentGeneric.as_view()),
    path('generic-student/<id>/', StudentGeneric1.as_view()),
    path('student/', StudentAPI.as_view(), name='student'),
    # path('', home, name='home'),
    # path('student/', post_student, name='post_student'),
    # path('update/<id>/', update_student, name='update_student'),
    # path('delete/<id>/', delete_student, name='delete_student'),
    path('get-book/', get_book),
    path('register/', RegisterUser.as_view(), name='register'),


]
