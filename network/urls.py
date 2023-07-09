
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:username>", views.userpage, name="userpage"),
    path("following", views.following_posts, name="following_posts"),
    
    #API routes
    path("follow/<str:username>", views.follow_user, name="follow_user"),
    path("followers-number/<str:username>", views.get_number_of_followers, name="get_number_of_followers"),
    path("update-post/<int:id>", views.update_post, name="update_post"),
    path("get-new-post/<int:id>", views.get_new_post, name="get_new_post"),
    path("like-post/<int:id>", views.like_post, name="like_post"),
    path("get-number-of-likes/<int:id>", views.get_number_of_likes, name="get_number_of_likes")
]
