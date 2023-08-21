import re

import requests
from bs4 import BeautifulSoup


def get_html_page(url_link: str) -> str:
    response = requests.get(url_link)
    result = ""

    if response.status_code == requests.codes.all_ok:
        result = response.text

    return result


class PageInfoGetter:
    def __init__(self, html_text: str):
        self.__soup = BeautifulSoup(html_text, "html.parser")

    def get_title(self):
        return self.__do_get("title")

    def get_description(self):
        return self.__do_get("description")

    def get_type(self):
        type_str = self.__do_get("type")
        search_res = re.search(r"(\w+)\..*", type_str)
        result = "website"

        if search_res:
            result = search_res.group(1)

        return result

    def get_image(self):
        return self.__do_get("image")

    def __do_get(self, name: str):
        element = self.__soup.find("meta", property=f"og:{name}")
        result = None

        if not element:
            element = self.__soup.find("meta", {"name": name})

        if element:
            result = element.get("content")

        return result
