from django.contrib import admin
from django.urls import path, re_path
from .views import *


urlpatterns = [
    re_path(r'^History/?$', HistoryCreateAPIView.as_view()),
    re_path(r'^History/(?P<pk>\d+)/?$', HistoryRetrieveUpdateAPIView.as_view()),
    re_path(r'^History/Account/(?P<pk>\d+)/?$', GetHistoryView.as_view()),
    
]