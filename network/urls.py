
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("upload/<str:username>", views.upload, name="upload"),
    path("edit/<int:user_id>/<int:post_id>", views.edit, name="edit"),
    path("like/<int:post_id>", views.like, name="like"),
    path("following", views.following, name="following"),
    path("connect/<int:profile_user>", views.connect, name="connect")
    
]
