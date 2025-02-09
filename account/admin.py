from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from django.contrib.auth.models import User


admin.site.register(models.Relation)
admin.site.unregister(User)

class ProfileInLine(admin.StackedInline):
    model = models.UserBio
class ExtendedUserAdmin(UserAdmin):
    inlines = (ProfileInLine,)

admin.site.register(User, ExtendedUserAdmin)