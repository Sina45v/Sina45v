from django.contrib import admin
from . import models

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at", "updated_at", "author"]
    search_fields = ["title"]
    list_filter = ["created_at"]
    raw_id_fields = ["author"]

admin.site.register(models.Comment)