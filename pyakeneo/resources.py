import json
import math


from pyakeneo import interfaces
from pyakeneo.result import Result
from pyakeneo.utils import urljoin


class CreatableResource(interfaces.CreatableResourceInterface):
    def create_item(self, item):
        url = self._endpoint
        r = self._session.post(url, data=json.dumps(item, separators=(",", ":")))

        r.raise_for_status()


class ListableResource(interfaces.ListableResourceInterface):
    def fetch_list(self, args=None):
        """Send a request with search, etc.
        Returns an iterable list (Collection)"""
        if args:
            for key, value in args.items():
                if not isinstance(value, str):
                    args[key] = json.dumps(value)

        url = self._endpoint
        r = self._session.get(url, params=args)
        r.raise_for_status()

        c = Result.from_json_text(self._session, json_text=r.text)
        return c


class SearchAfterListableResource(ListableResource):
    def fetch_list(self, args=None):
        """Send a request with search, etc.
        Returns an iterable list (Collection)"""
        params = args
        if not params:
            params = {"pagination_type": "search_after"}
        elif "pagination_type" not in params:
            params["pagination_type"] = "search_after"

        return super(SearchAfterListableResource, self).fetch_list(params)


class GettableResource(interfaces.GettableResourceInterface):
    def fetch_item(self, code_or_item):
        """Returns a unique item object. code_or_item should be the code
        of the desired item, or an item with the proper code."""
        code = code_or_item
        if not isinstance(code_or_item, str):
            # if code_or_item is item, then fetch the code
            code = self.get_code(code_or_item)

        url = urljoin(self._endpoint, code)
        r = self._session.get(url)
        r.raise_for_status()

        return json.loads(r.text)  # returns item as a dict


class DeletableResource(interfaces.DeletableResourceInterface):
    def delete_item(self, code_or_item):
        """code_or_item should be the code
        of the desired item, or an item with the proper code."""
        code = code_or_item
        if not isinstance(code_or_item, str):
            # if code_or_item is item, then fetch the code
            code = self.get_code(code_or_item)
        url = urljoin(self._endpoint, code)
        r = self._session.delete(url)

        r.raise_for_status()


class UpdatableResource(interfaces.UpdatableResourceInterface):
    def update_create_item(self, item_values, code=None):
        if not code:
            code = self.get_code(item_values)

        url = urljoin(self._endpoint, code)
        r = self._session.patch(
            url, data=json.dumps(item_values, separators=(",", ":"))
        )
        r.raise_for_status()

        return r.headers.get("Location")


class UpdatableListResource(interfaces.UpdatableResourceInterface):
    def update_create_list(self, items, code=None):
        url = self._endpoint
        data = ""
        for item in items:
            data += json.dumps(item, separators=(",", ":")) + "\n"
        r = self._session.patch(
            url,
            data=data,
            headers={"Content-type": "application/vnd.akeneo.collection+json"},
        )

        if r.status_code == 413:
            # TODO handle 413
            # Request Entity Too Large
            # There are too many resources to process (max 100)
            # =>>>>> or the line of JSON is too long (max 1 000 000 characters)
            # split the list in several chunks
            num = 100
            n = math.ceil(len(items) / num)

            itemss = [items[i : i + num] for i in range(0, (n - 1) * num, num)]
            itemss.append(items[(n - 1) * num :])

            return [
                item
                for those_items in itemss
                for item in self.update_create_list(those_items)
            ]

        r.raise_for_status()

        statuses = []
        for line in r.text.split("\n"):
            statuses.append(json.loads(line))
        return statuses


class IdentifierBasedResource(interfaces.CodeBasedResourceInterface):
    def get_code(self, item):
        return item["identifier"]


class CodeBasedResource(interfaces.CodeBasedResourceInterface):
    def get_code(self, item):
        return item["code"]


class EnterpriseEditionResource:
    pass


class ResourcePool:
    def __init__(self, endpoint, session):
        """Initialize the ResourcePool to the given endpoint. Eg: products"""
        self._endpoint = endpoint
        self._session = session

    def get_url(self):
        return self._endpoint


class ProductsPool(
    ResourcePool,
    IdentifierBasedResource,
    CreatableResource,
    DeletableResource,
    GettableResource,
    SearchAfterListableResource,
    UpdatableResource,
    UpdatableListResource,
):
    """https://api.akeneo.com/api-reference.html#Products"""

    # TODO: EE support of drafts
    pass


class ProductModelsPool(
    ResourcePool,
    IdentifierBasedResource,
    CreatableResource,
    GettableResource,
    SearchAfterListableResource,
    UpdatableResource,
):
    """https://api.akeneo.com/api-reference.html#Productmodel"""

    pass


class PublishedProductsPool(
    ResourcePool,
    IdentifierBasedResource,
    GettableResource,
    SearchAfterListableResource,
    EnterpriseEditionResource,
):
    """https://api.akeneo.com/api-reference.html#Publishedproduct"""

    pass


class CategoriesPool(
    ResourcePool,
    CodeBasedResource,
    CreatableResource,
    GettableResource,
    ListableResource,
    UpdatableResource,
    UpdatableListResource,
):
    """https://api.akeneo.com/api-reference.html#Category"""

    pass


class FamilyVariantsPool(
    ResourcePool,
    CodeBasedResource,
    CreatableResource,
    GettableResource,
    ListableResource,
):
    """https://api.akeneo.com/api-reference.html#Familyvariant"""

    pass


class FamiliesPool(
    ResourcePool,
    CodeBasedResource,
    CreatableResource,
    DeletableResource,
    GettableResource,
    ListableResource,
    UpdatableResource,
    UpdatableListResource,
):
    """https://api.akeneo.com/api-reference.html#Family"""

    def variants(self, code):
        return FamilyVariantsPool(
            urljoin(self._endpoint, code, "variants/"), self._session
        )


class AttributeOptionsPool(
    ResourcePool,
    CodeBasedResource,
    CreatableResource,
    GettableResource,
    ListableResource,
    UpdatableResource,
):
    """https://api.akeneo.com/api-reference.html#Attributeoptions"""

    pass


class AttributesPool(
    ResourcePool,
    CodeBasedResource,
    CreatableResource,
    GettableResource,
    ListableResource,
    UpdatableResource,
    UpdatableListResource,
):
    """https://api.akeneo.com/api-reference.html#Attributes"""

    def options(self, code):
        return AttributeOptionsPool(
            urljoin(self._endpoint, code, "options/"), self._session
        )


class AttributeGroupsPool(
    ResourcePool,
    CodeBasedResource,
    ListableResource,
    CreatableResource,
    UpdatableListResource,
    GettableResource,
    UpdatableResource,
):
    """https://api.akeneo.com/api-reference.html#Attributegroups"""

    pass


class MediaFilesPool(
    ResourcePool,
    CodeBasedResource,
    ListableResource,
    CreatableResource,
    GettableResource,
):
    """https://api.akeneo.com/api-reference.html#Mediafiles"""

    def download(self, code):
        # TODO: implement this method
        raise NotImplementedError()


class LocalesPool(
    ResourcePool,
    CodeBasedResource,
    ListableResource,
    GettableResource,
):
    """https://api.akeneo.com/api-reference.html#Locales"""

    pass


class ChannelsPool(
    ResourcePool,
    CodeBasedResource,
    ListableResource,
    UpdatableListResource,
    GettableResource,
    UpdatableResource,
):
    """https://api.akeneo.com/api-reference.html#Channels"""

    pass


class CurrenciesPool(
    ResourcePool,
    CodeBasedResource,
    ListableResource,
    CreatableResource,
):
    """https://api.akeneo.com/api-reference.html#Currencies"""

    pass


class MeasureFamiliesPool(
    ResourcePool,
    CodeBasedResource,
    ListableResource,
    GettableResource,
):
    """https://api.akeneo.com/api-reference.html#Measurefamilies"""

    pass


class AssociationTypesPool(
    ResourcePool,
    CodeBasedResource,
    ListableResource,
    CreatableResource,
    UpdatableListResource,
    GettableResource,
    UpdatableResource,
):
    """https://api.akeneo.com/api-reference.html#Associationtypes"""

    pass


class AssetsPool(
    ResourcePool,
    CodeBasedResource,
    GettableResource,
    ListableResource,
    UpdatableResource,
    UpdatableListResource,
    DeletableResource,
):
    pass


class AssetFamilyPool(
    ResourcePool,
    CodeBasedResource,
    GettableResource,
    ListableResource,
    UpdatableResource,
):
    def assets(self, code):
        return AssetsPool(urljoin(self._endpoint, code, "assets/"), self._session)


class ReferenceEntityRecordPool(
    ResourcePool,
    CodeBasedResource,
    GettableResource,
    ListableResource,
    UpdatableResource,
    UpdatableListResource,
):
    pass


class ReferenceEntityAttributeOptionsPool(
    ResourcePool,
    CodeBasedResource,
    GettableResource,
    ListableResource,
    UpdatableResource,
):
    pass


class ReferenceEntityAttributePool(
    ResourcePool,
    CodeBasedResource,
    GettableResource,
    ListableResource,
    UpdatableResource,
):
    def options(self, code):
        return ReferenceEntityAttributeOptionsPool(
            urljoin(self._endpoint, code, "options/"), self._session
        )


class ReferenceEntityPool(
    ResourcePool,
    CodeBasedResource,
    GettableResource,
    ListableResource,
    UpdatableResource,
):
    def records(self, entity_code):
        return ReferenceEntityRecordPool(
            urljoin(self._endpoint, entity_code, "records/"), self._session
        )

    def attributes(self, entity_code):
        return ReferenceEntityAttributePool(
            urljoin(self._endpoint, entity_code, "attributes/"), self._session
        )
