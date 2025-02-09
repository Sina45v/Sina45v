from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path("posts/<int:post_id>", views.PostView.as_view(), name='post'),
    path("post/<int:post_id>/delete", views.PostDeleteView.as_view(), name='post_delete'),
    path("posts/<int:post_id>/update", views.PostUpdateView.as_view(), name='post_update'),
    path("posts/create", views.PostCreateView.as_view(), name='post_create'),
    path("reply/<int:post_id>/<int:comment_id>", views.ReplyView.as_view(), name='reply_create'),
    path("like/<int:post_id>", views.LikeView.as_view(), name="like"),
    path("dislike/<int:post_id>", views.DissLikeView.as_view(), name="dislike"),
    path("about", views.AboutView.as_view(), name="about"),
]
