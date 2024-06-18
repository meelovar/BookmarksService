from celery import shared_task

from bookmarks.models import Bookmark
from bookmarks.services import PageInfoGetter, get_html_page


@shared_task
def get_page_info(bookmark_pk):
    bookmark = Bookmark.objects.get(pk=bookmark_pk)
    page_info = PageInfoGetter(get_html_page(bookmark.link))

    bookmark.title = page_info.get_title()
    bookmark.description = page_info.get_description()
    bookmark.preview_image = page_info.get_image()
    bookmark.link_type = page_info.get_type()

    bookmark.save()
