from django.contrib import admin
from django.urls import include, path, re_path
from core import views as core_views
from django.contrib.auth import views as auth_views
from blockchain import views as blockchain_views

urlpatterns = [
    path("", core_views.Home.as_view(), name="home"),
    path("oldadmin/", admin.site.urls),
    # path("admin/", include("admin_page.urls")),
    path("createconvict/", core_views.CreateConvict.as_view(), name="createconvict"),
    path("createblock/", core_views.CreateBlock.as_view(), name="createblock"),
    path("convict/<int:pk>/", core_views.ConvictDetailView.as_view(), name="convictdetail"),
    path(
        "convict/<int:pk>/validate/create/",
        core_views.ConvictValidateCreateView.as_view(),
        name="convictvalidate_create",
    ),
    path("block/<int:pk>/validate/create/", core_views.BlockValidateCreateView.as_view(), name="blockvalidate_create"),
    path("block/<int:pk>/", core_views.BlockDetailView.as_view(), name="blockdetail"),
    path("search/", core_views.SearchView.as_view(), name="search"),
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="core/logout.html"), name="logout"),
    path("our-team/", core_views.Home.as_view(template_name="core/team-details.html"), name="ourteam"),
    path("community/", core_views.Home.as_view(template_name="core/community.html"), name="community"),
    path("thankyou/", core_views.Home.as_view(template_name="core/thankyou.html"), name="thankyou"),
    # path("faq/", core_views.Home.as_view(template_name="core/faq.html"), name="faq"),
    # path("blog/", core_views.Home.as_view(template_name="core/blog.html"), name="blog"),
    # path("blogdetail/", core_views.Home.as_view(template_name="core/blog-details.html"), name="blog-details"),
    path("contact/", core_views.Home.as_view(template_name="core/contact.html"), name="contact"),
    path("404/", core_views.Home.as_view(template_name="core/404.html"), name="404"),
    # re_path("^savedata", blockchain_views.saveToFile, name="saveToFile"),
    re_path("^get_chain$", blockchain_views.get_chain, name="get_chain"),
    re_path("^mine_block$", blockchain_views.mine_block, name="mine_block"),  # type: ignore
    re_path("^add_transaction$", blockchain_views.add_transaction, name="add_transaction"),  # type: ignore
    re_path("^is_valid$", blockchain_views.is_valid, name="is_valid"),
    re_path("^connect_node$", blockchain_views.connect_node, name="connect_node"),  # type: ignore
    re_path("^replace_chain$", blockchain_views.replace_chain, name="replace_chain"),
]
handler404 = "core.views.page_not_found_view"
