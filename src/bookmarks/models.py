from django.db import models
from django.contrib import auth

UserModel = auth.get_user_model()


class Bookmark(models.Model):
    class LinkType(models.TextChoices):
        Website = "website"
        Book = "book"
        Article = "article"
        Music = "music"
        Video = "video"

    title = models.CharField(max_length=256, default="")
    description = models.TextField(max_length=512, default="")
    link = models.URLField(max_length=512)
    link_type = models.CharField(max_length=32, choices=LinkType.choices, default=LinkType.Website)
    preview_image = models.URLField(default="")
    created_by = models.ForeignKey(UserModel, models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{super().__str__()}: {self.link}"


class Collection(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    bookmarks = models.ManyToManyField(Bookmark, "collections")
    created_by = models.ForeignKey(UserModel, models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{super().__str__()}: {self.title}"
