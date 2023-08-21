from django.urls import include, path
from rest_framework import routers

from bookmarks import views

router = routers.DefaultRouter()

router.register("bookmarks", views.BookmarkViewSet, "bookmarks")
router.register("collections", views.CollectionViewSet, "collections")
router.register(r"collections/(?P<id>\d+)/bookmarks", views.BookmarkCollectionViewSet, "bookmarks-collections")

urlpatterns = [
    path("", include(router.urls)),
    # path("collections/<int:id>/bookmarks/", views.BookmarkCollectionViewSet.as_view()),
    # path("bookmarks/", views.BookmarkView.as_view(), name="bookmarks"),
    # path("collections/", views.CollectionView.as_view(), name="collections"),
]
