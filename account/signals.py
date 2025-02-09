from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import UserBio




def logincreateUserBio(sender, **kwargs):
    if kwargs['created']:
        UserBio.objects.create(user=kwargs['instance'])

post_save.connect(receiver=logincreateUserBio, sender=User)