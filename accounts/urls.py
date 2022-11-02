from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [


    path('register/', RegisterView.as_view()),
    path('verify/', VerifyOtp.as_view()),


]
