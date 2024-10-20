from django.contrib import admin
from django.urls import path, re_path
from .views import *
from django.urls import path, include

urlpatterns = [
    re_path(r'^api/History/?$', HistoryCreateAPIView.as_view()),
    re_path(r'^api/History/(?P<pk>\d+)/?$', HistoryRetrieveUpdateAPIView.as_view()),
    re_path(r'^api/History/Account/(?P<pk>\d+)/?$', GetHistoryView.as_view()),
]
