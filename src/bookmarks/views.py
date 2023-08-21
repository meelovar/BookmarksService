from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response
from bookmarks.permissions import IsOwner

from bookmarks.models import Bookmark, Collection
from bookmarks.serializers import BookmarkCollectionSerializer, BookmarkSerializer, CollectionSerializer


class BaseMixin(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    pass


class BookmarkViewSet(BaseMixin, viewsets.GenericViewSet):
    permission_classes = [IsOwner]
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()

    def get_queryset(self):
        user = self.request.user

        return Bookmark.objects.filter(created_by=user)


class CollectionViewSet(BaseMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsOwner]
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

    def get_queryset(self):
        user = self.request.user

        return Collection.objects.prefetch_related("bookmarks").filter(created_by=user)


class BookmarkCollectionViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsOwner]
    serializer_class = BookmarkCollectionSerializer
    queryset = Bookmark.objects.all()

    def get_queryset(self):
        user = self.request.user
        collection_id = self.kwargs.get("id")

        return Bookmark.objects.filter(created_by=user, collection=collection_id)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        collection_id = self.kwargs.get("id")
        collection_qs = Collection.objects.prefetch_related("bookmarks")
        collection = generics.get_object_or_404(collection_qs, created_by=user, pk=collection_id)
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        bookmark_id = serializer.validated_data["id"]
        bookmark = generics.get_object_or_404(Bookmark.objects.all(), created_by=user, pk=bookmark_id)

        collection.bookmarks.add(bookmark)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
