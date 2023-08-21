from rest_framework import serializers

from bookmarks.models import Bookmark, Collection
from bookmarks.services import PageInfoGetter, get_html_page


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
        link = validated_data.get("link")
        user = self.context["request"].user
        page_info = PageInfoGetter(get_html_page(link))

        validated_data["created_by"] = user
        validated_data["title"] = page_info.get_title()
        validated_data["description"] = page_info.get_description()
        validated_data["preview_image"] = page_info.get_image()
        validated_data["link_type"] = page_info.get_type()

        return super().create(validated_data)


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
