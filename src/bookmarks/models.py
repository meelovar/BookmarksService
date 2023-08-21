from django.db import models
from django.contrib import auth


class Bookmark(models.Model):
    class LinkType(models.TextChoices):
        Website = "website"
        Book = "book"
        Article = "article"
        Music = "music"
        Video = "video"

    title = models.CharField(max_length=256, null=True)
    description = models.TextField(max_length=512, null=True)
    link = models.URLField(max_length=512)
    link_type = models.CharField(max_length=32, choices=LinkType.choices, default=LinkType.Website)
    preview_image = models.URLField(null=True)
    created_by = models.ForeignKey(auth.get_user_model(), models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)


class Collection(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    bookmarks = models.ManyToManyField(Bookmark, "collections")
    created_by = models.ForeignKey(auth.get_user_model(), models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
