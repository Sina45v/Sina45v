from django.urls import path
from . import views
app_name = "account"
urlpatterns = [
    path("register", views.UserRegisterView.as_view(), name="register"),
    path("login", views.UserLoginView.as_view(), name="login"),
    path("logout", views.UserLogoutView.as_view(), name="logout"),
    path("profile/<int:user_id>", views.UserProfileView.as_view(), name="profile"),
    path("password-reset", views.PassResetView.as_view(), name="password_reset"),
    path("password-reset/done", views.PassResetDoneView.as_view(), name="password_reset_done"),
    path("confirm/<uidb64>/<token>", views.PassResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset/complete", views.PassResetCompleteView.as_view(), name="password_reset_complete"),
    path("follow/<int:user_id>", views.FollowView.as_view(), name="follow"),
    path("unfollow/<int:user_id>", views.UnFollowView.as_view(), name="unfollow"),
    path("edit-profile", views.EditProfileView.as_view(), name="edit_profile"),

]