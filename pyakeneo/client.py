import requests
from pyakeneo.auth import Auth
from pyakeneo.resources import (AssetFamilyPool, AssociationTypesPool,
                                AttributeGroupsPool, AttributesPool,
                                CategoriesPool, ChannelsPool, CurrenciesPool,
                                FamiliesPool, LocalesPool, MeasureFamiliesPool,
                                MediaFilesPool, ProductModelsPool,
                                ProductsPool, PublishedProductsPool,
                                ReferenceEntityPool)
from pyakeneo.utils import urljoin


class Client:
    BASIC_API_PATH = "/api/rest/v1/"

    def __init__(
            self,
            base_url: str,
            client_id: str = None,
            secret: str = None,
            username: str = None,
            password: str = None,
            session: requests.Session = None,
    ):
        if not session and not (client_id and secret and username and password):
            # No credentials provided neither via client_id+secret+username+password nor via session
            raise ValueError(
                "Expect credentials via "
                + "1) as client_id+secret+username+password, or "
                + "2) as session having an authentication."
            )

        if not session:
            session = requests.Session()
            session.auth = self._make_auth(base_url, client_id, secret, username, password)

        self._init(base_url, session)

    def _make_auth(self, base_url, client_id, secret, username, password) -> Auth:
        return Auth(base_url, client_id, secret, username, password)

    def _init(self, base_url, session):
        self._base_url = base_url
        self._session = session
        self._session.headers.update({"Content-Type": "application/json"})
        self._resources = {
            "association_types": AssociationTypesPool(
                urljoin(self._base_url, self.BASIC_API_PATH, "association-types/"),
                session,
            ),
            "attributes": AttributesPool(
                urljoin(self._base_url, self.BASIC_API_PATH, "attributes/"), session
            ),
            "attribute_groups": AttributeGroupsPool(
                urljoin(self._base_url, self.BASIC_API_PATH, "attribute-groups/"),
                session,
            ),
            "categories": CategoriesPool(
                urljoin(self._base_url, self.BASIC_API_PATH, "categories/"), session
            ),
            "channels": ChannelsPool(
                urljoin(self._base_url, self.BASIC_API_PATH, "channels/"), session
            ),
            "currencies": CurrenciesPool(
                urljoin(self._base_url, self.BASIC_API_PATH, "currencies/"), session
            ),
            "families": FamiliesPool(
                urljoin(self._base_url, self.BASIC_API_PATH, "families/"), session
            ),
            "locales": LocalesPool(
                urljoin(self._base_url, self.BASIC_API_PATH, "locales/"), session
            ),
            "measure_families": MeasureFamiliesPool(
                urljoin(self._base_url, self.BASIC_API_PATH, "measure-families/"),
                session,
            ),
            "media_files": MediaFilesPool(
                urljoin(self._base_url, self.BASIC_API_PATH, "media-files/"), session
            ),
            "products": ProductsPool(
                urljoin(self._base_url, self.BASIC_API_PATH, "products/"), session
            ),
            "product_models": ProductModelsPool(
                urljoin(self._base_url, self.BASIC_API_PATH, "product-models/"), session
            ),
            "published_products": PublishedProductsPool(
                urljoin(self._base_url, self.BASIC_API_PATH, "published-products/"),
                session,
            ),
            "asset_families": AssetFamilyPool(
                urljoin(self._base_url, self.BASIC_API_PATH, "asset-families/"), session
            ),
            "reference_entities": ReferenceEntityPool(
                urljoin(self._base_url, self.BASIC_API_PATH, "reference-entities/"),
                session,
            ),
        }

    @property
    def resources(self):
        """Return all resources as a list of Resources"""
        return self._resources

    @property
    def association_types(self):
        return self._resources["association_types"]

    @property
    def attributes(self):
        return self._resources["attributes"]

    @property
    def attribute_groups(self):
        return self._resources["attribute_groups"]

    @property
    def categories(self):
        return self._resources["categories"]

    @property
    def channels(self):
        return self._resources["channels"]

    @property
    def currencies(self):
        return self._resources["currencies"]

    @property
    def families(self):
        return self._resources["families"]

    @property
    def locales(self):
        return self._resources["locales"]

    @property
    def measure_families(self):
        return self._resources["measure_families"]

    @property
    def media_files(self):
        return self._resources["media_files"]

    @property
    def products(self):
        return self._resources["products"]

    @property
    def product_models(self):
        return self._resources["product_models"]

    @property
    def published_products(self):
        return self._resources["published_products"]

    @property
    def asset_families(self):
        return self._resources["asset_families"]

    @property
    def reference_entities(self):
        return self._resources["reference_entities"]
