from __future__ import annotations

import json
from typing import Dict, Iterable

import requests


class Result(object):
    """
    Holds the result of a search. It can be iterated through as a list,
    as an iterator, or as a generator. Note that only one iteration should be
    used on a given Collection object.
    Search results are paginated: https://api.akeneo.com/documentation/pagination.html

    The next page will be loaded once the user iterated over the whole current page.
    The content of the new page will replace the content of the previous page.
    """

    def __init__(
        self,
        session: requests.Session,
        *,
        items: list | dict,
        count: int,
        link_first: str,
        link_next: str,
        link_self: str,
    ):
        self._session = session
        self._items = items
        self._count = count
        self._link_next = link_next
        self._link_self = link_self
        self._link_first = link_first

        self._page_iterator = iter(self._items)
        self._reached_the_end = False

    def __iter__(self):
        while not self._reached_the_end:
            for item in self._page_iterator:
                yield item
            self.fetch_next_page()

    def __next__(self):
        try:
            return next(self._page_iterator)
        except StopIteration:
            self.fetch_next_page()
            if not self._reached_the_end:
                return next(self._page_iterator)
            else:
                return

    def get_page_items(self):
        return self._items

    def fetch_next_page(self):
        """Return True if a next page exists. Returns False otherwise."""
        if self._link_next:
            response = self._session.get(self._link_next)
            if response.ok:
                next_page = Result.parse_page(json.loads(response.text))
                self._items = next_page["items"]
                self._count = next_page["count"]
                self._link_next = next_page["link_next"]
                self._link_self = next_page["link_self"]
                self._link_first = next_page["link_first"]

                self._page_iterator = iter(self._items)
                self._reached_the_end = False
            else:
                self._reached_the_end = True
        else:
            self._reached_the_end = True
        return not self._reached_the_end

    def get_count(self):
        return self._count

    def get_next_link(self):
        return self._link_next

    def get_self_link(self):
        return self._link_self

    def get_first_link(self):
        return self._link_first

    @classmethod
    def parse_page(cls, json_data: dict) -> Dict:
        """Returns (next link, retrieved items, count of items)"""
        final_next_link = None
        next_link = json_data["_links"].get("next")
        if next_link:
            final_next_link = next_link["href"]
        return {
            "items": json_data["_embedded"]["items"],
            "count": json_data.get("items_count"),
            "link_first": json_data["_links"]["first"]["href"],
            "link_next": final_next_link,
            "link_self": json_data["_links"]["self"]["href"],
        }

    @classmethod
    def parse_result(cls, session: requests.Session, json_data: dict | list):
        if cls.is_paginated(json_data):
            return cls(session, **cls.parse_page(json_data))
        else:
            return cls(session, **cls.parse_non_paginated(json_data))

    @staticmethod
    def from_json_text(session: requests.Session, json_text: str) -> "Result":
        json_data = json.loads(json_text)
        return Result.parse_result(session, json_data)

    @classmethod
    def is_paginated(cls, json_data: dict | list):
        return isinstance(json_data, dict) and "_links" in json_data

    @classmethod
    def parse_non_paginated(cls, json_data: list) -> Dict:
        link_self = ""
        if json_data and "_links" in json_data[0]:
            link_self = json_data[0]["_links"]["self"]["href"]
        return {
            "items": json_data,
            "count": len(json_data),
            "link_first": "",
            "link_next": "",
            "link_self": link_self,
        }
