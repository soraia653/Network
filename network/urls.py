
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile_page/<str:username>", views.profile_page, name="profile"),
    path("following", views.following, name="following"),

    # API routes
    path("edit_post/<int:post_id>", views.edit_post, name="new_post"),
    path("like_post/<int:post_id>", views.like_post, name="like")
]
