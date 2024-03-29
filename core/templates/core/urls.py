from django.contrib import admin
from django.urls import path
from core import views as core_views
from django.contrib.auth import views as auth_views

# its not working for others
urlpatterns = [
    path("", core_views.Home.as_view(), name="home"),
    path("createconvict/", core_views.CreateConvict.as_view(), name="createconvict"),
    path("createblock/", core_views.CreateBlock.as_view(), name="createblock"),
    path("convict/<int:pk>/", core_views.ConvictDetailView.as_view(), name="convictdetail"),
    path("block/<int:pk>/", core_views.BlockDetailView.as_view(), name="blockdetail"),
    path("search/", core_views.SearchView.as_view(), name="search"),
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="core/logout.html"), name="logout"),
    path("our-team/", core_views.Home.as_view(template_name="team-details.html"), name="ourteam"),
    # path("contact/", core_views.Home.as_view(template_name="thankyou.html"), name="contact"),
]
