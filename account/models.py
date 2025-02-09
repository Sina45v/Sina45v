from django.db import models
from django.contrib.auth.models import User


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='follower')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='following')

    def __str__(self):
        return f"{self.from_user} is following {self.to_user}"


class UserBio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
