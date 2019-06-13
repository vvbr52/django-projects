from django.urls import path
from . import views
# from sili.views import home, get_response
app_name = 'bot'


urlpatterns = [
    path('', views.home),
    path('get-response/', views.get_response),
]
# -*- coding: utf-8 -*-

