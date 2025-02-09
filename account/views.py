from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from home.models import Post
from . import forms
from home import models as home_models
from home import forms as home_forms
from . import models
from .models import Relation


class UserRegisterView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    form_class = forms.UserRegisterForm
    template_name = 'account/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            user = User.objects.create_user(username=clean_data['username'],
                                     email=clean_data['email'],
                                     password=clean_data['password'])
            messages.success(request, 'Account created successfully',
                             "success")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend' )
            return redirect('home:home')
        return render(request, self.template_name, context={"form": form})


class UserLoginView(View):
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    form_class = forms.UserLoginForm
    template_name = 'account/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            authenticated_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, 'logged in successfully', "success")
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'Username or password is incorrect',
                           "error")
        return render(request, self.template_name, context={"form": form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully', "success")
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        form = home_forms.SearchForm()
        posts = user.posts.all()
        followed = user.following.filter(from_user=request.user).exists()
        followers = user.following.count()
        following = user.follower.count()
        if request.GET.get("search"):
            posts = posts.filter(title__icontains=request.GET["search"])
        return render(request, "account/profile.html", context={"user": user,
                                                                "posts": posts,
                                                                "followed": followed,
                                                                "followers": followers,
                                                                "form": form,
                                                                "following": following})


class PassResetView(auth_views.PasswordResetView):
    template_name = "account/password_reset_form.html"
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = "account/password_reset_email.html"


class PassResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "account/password_reset_done.html"


class PassResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "account/password_reset_confirm.html"
    success_url = reverse_lazy("account:password_reset_complete")


class PassResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "account/password_reset_complete.html"


class FollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user,
                                           to_user=user)
        if relation.exists():
            messages.error(request, 'You are already following this user',
                           "error")
        else:
            Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request, 'You are now following this user',
                             "success")
        return redirect('account:profile', user_id)


class UnFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user,
                                           to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'You unfollowed this user', "success")
        else:
            messages.error(request, 'You are not following this user', "error")
        return redirect('account:profile', user_id)


class EditProfileView(LoginRequiredMixin, View):

    def get(self, request):
        form = forms.EditProfileForm(instance=request.user.userbio, initial={'email': request.user.email})
        return render(request, "account/editprofile.html", context={"form":form})

    def post(self, request):
        form = forms.EditProfileForm(request.POST,
                                     instance=request.user.userbio, )
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'Profile updated successfully',)
            return redirect('account:profile', request.user.id)
        return render("editprofile.html", {"form": form})