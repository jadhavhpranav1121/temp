from django.contrib import admin
from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    re_path("", admin_login, name="admin_login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("convict/", convict, name="convict"),
    path("blocks/", Block, name="Block"),
]
