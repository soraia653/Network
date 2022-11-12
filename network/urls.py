
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile_page", views.profile_page, name="profile"),

    # API routes
    path("all-posts", views.all_posts, name="all-posts")
]
