from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts')

    class Meta:
        ordering = ['-created_at', "content"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("home:post", args=[self.id])

    def is_liked(self, user):
        liked = self.postlike.filter(user=user)
        if liked.exists():
            liked.delete()

    def is_dissliked(self, user):
        dissliked = self.postdislike.filter(user=user)
        if dissliked.exists():
            dissliked.delete()

    def get_comment_count(self):
        """Instance method to get comment count for this specific post"""
        return self.postcomments.count()

    def get_like_count(self):
        return self.postlike.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='usercomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='postcomments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey("Comment", on_delete=models.CASCADE,
                              related_name='replies', blank=True, null=True)
    is_reply = models.BooleanField(default=False)

    def __str__(self):
        return f"user{self.user} commented {self.body[:25]} at {self.created_at}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='userlike')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='postlike')

    def __str__(self):
        return f"user{self.user} liked {self.post}"


class DissLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='userdislike')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='postdislike')

    def __str__(self):
        return f"user{self.user} disliked {self.post}"
