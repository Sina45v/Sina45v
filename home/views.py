from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from . import models, forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class HomeView(View):
    def get(self, request):
        form = forms.SearchForm()
        posts = models.Post.objects.all()
        user = request.user
        if request.GET.get('search'):
            posts = posts.filter(content__icontains=request.GET['search'])
        return render(request, "home/home.html", context={"user":user, "posts":posts, "form":form})


from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class PostView(View):
    def get(self, request, post_id):
        """
        Handle GET requests for post detail page
        """
        # Get the post object or return 404
        post = get_object_or_404(models.Post, pk=post_id)
        # Get top-level comments (exclude replies) ordered by creation date
        comments = models.Comment.objects.filter(post=post,is_reply=False).order_by('-created_at')
        likes = models.Like.objects.filter(post=post).count()
        disslikes = models.DissLike.objects.filter(post=post).count()
        # Initialize empty forms
        comment_form = forms.CommentCreateForm()
        reply_form = forms.CommentReplyForm()
        return render(request, "home/post.html", {'post':post, 'comments':comments, 'comment_form':comment_form,
                                                  'reply_form':reply_form, 'disslikes':disslikes, 'likes':likes})
    @method_decorator(login_required)
    def post(self, request, post_id):
        """
        Handle POST requests for new comments
        """
        # Get the post object or return 404
        post = get_object_or_404(models.Post, pk=post_id)
        # Initialize form with POST data
        form = forms.CommentCreateForm(request.POST)
        if form.is_valid():
            # Create comment object without saving to DB
            new_comment = form.save(commit=False)
            # Set additional fields
            new_comment.user = request.user  # Set logged-in user
            new_comment.post = post  # Associate with current post
            new_comment.is_reply = False  # Ensure it's a top-level comment
            # Save to database
            new_comment.save()
            # Success message
            messages.success(request, "Comment posted successfully!")
            # Redirect to prevent duplicate submissions
            return redirect('home:post', post_id=post.id)
        else:
            # If form is invalid, show errors
            messages.error(request, "Error posting comment. Please check the form.")
            # Get existing comments and forms again
            comments = models.Comment.objects.filter(post=post, is_reply=False).order_by('-created_at')
            reply_form = forms.CommentReplyForm()
            return render(request, "home/post.html", {
                'post': post,
                'comments': comments,
                'comment_form': form,  # Pass invalid form with errors
                # 'reply_form': reply_form
})

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(models.Post, pk=post_id)
        if request.user.id == post.author.id:
            post.delete()
            messages.success(request, "Post deleted successfully")
        else:
            messages.error(request, "You do not have permission to delete this post")
        return redirect("account:profile", request.user.id)

class PostUpdateView(LoginRequiredMixin, View):
    form_class = forms.PostCreateUpdateForm
    def setup(self, request, *args, **kwargs):
        self.userpost = get_object_or_404(models.Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.userpost.author.id:
            messages.error(request, "You do not have permission to edit this post")
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.userpost)
        return render(request, "home/update.html", context={"form":form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.userpost)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully")
            return redirect("account:profile", request.user.id)
        return render(request, "home/update.html", context={"form":form})

class PostCreateView(LoginRequiredMixin, View):
    form_class = forms.PostCreateUpdateForm
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, "home/createpost.html", context={"form":form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            messages.success(request, "Post created successfully")
            return redirect("account:profile", request.user.id)
        return render(request, "home/createpost.html", context={"form":form})

class ReplyView(LoginRequiredMixin, View):
    form_class = forms.CommentReplyForm
    def post(self, request, post_id, comment_id):
        post = get_object_or_404(models.Post, pk=post_id)
        comment = get_object_or_404(models.Comment, pk=comment_id)
        form = forms.CommentReplyForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.reply = comment
            new_comment.is_reply = True
            new_comment.save()
        return redirect("home:post", post_id=post_id)

class LikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(models.Post, pk=post_id)
        post.is_dissliked(request.user)
        is_liked = models.Like.objects.filter(user=request.user)
        if is_liked.exists():
            is_liked.delete()
        else:
            models.Like.objects.create(user=request.user, post=post)
        return redirect("home:post", post_id)

class DissLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(models.Post, pk=post_id)
        post.is_liked(request.user)
        is_dissliked = models.DissLike.objects.filter(user=request.user)
        if is_dissliked.exists():
            is_dissliked.delete()
        else:
            models.DissLike.objects.create(user=request.user, post=post)
        return redirect("home:post", post_id)

class AboutView(View):
    def get(self, request):
        return render(request, "home/about.html")




















