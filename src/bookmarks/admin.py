from django.contrib import admin

from bookmarks.models import Bookmark, Collection


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    pass


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass
