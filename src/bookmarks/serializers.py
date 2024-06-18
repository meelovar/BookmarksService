from rest_framework import serializers

from bookmarks import tasks
from bookmarks.models import Bookmark, Collection


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ("id", "title", "description", "link", "link_type", "preview_image")
        extra_kwargs = {
            "title": {
                "read_only": True,
            },
            "description": {
                "read_only": True,
            },
            "link_type": {
                "read_only": True,
            },
            "preview_image": {
                "read_only": True,
            },
        }

    def create(self, validated_data):
        user = self.context["request"].user

        validated_data["created_by"] = user

        result = super().create(validated_data)

        tasks.get_page_info.delay(result.pk)

        return result


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ("id", "title", "description", "bookmarks")

    bookmarks = BookmarkSerializer(read_only=True, many=True)

    def create(self, validated_data):
        user = self.context["request"].user

        validated_data["created_by"] = user

        return super().create(validated_data)


class BookmarkCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ("id",)
        extra_kwargs = {
            "id": {
                "read_only": False,
            },
        }
