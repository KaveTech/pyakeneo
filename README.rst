|Build Status|
|Documentation Status|


Python client for Akeneo PIM API
================================

A simple Python client to use the `Akeneo PIM API`_.

Dependencies are managed with `poetry`_
(list of dependencies available in `pyproject.toml`_).

You may install them with:

.. code:: bashasda

        poetry install --dev

Installation
------------

.. code:: bash

        poetry install pyakeneo
        
Usage
-----

Initialization of the client

.. code:: python

        from pyakeneo.client import Client
        c = Client(
                AKENEO_URL, 
                username=AKENEO_USER, 
                password=AKENEO_PASSWORD,
                client_id=AKENEO_CLIENT_ID, 
                secret=AKENEO_SECRET,
        )

Then, you have a pool for every data type in Akeneo PIM.

.. code:: python

        # products
        c.products.fetch_item('ITEM_SKU')
        c.products.fetch_list({'limit': 100, 'page': 1, 'pagination_type': 'page'})

        # assets
        c.asset_families.assets('asset_family_code').fetch_item('ASSET_CODE')
        c.asset_families.assets('asset_family_code').fetch_list({'search': {"code":[{"operator":"IN","value":["CODE_1", "CODE_2"]}]}})

Tests
-----

Run tests as follow:

.. code:: bash

        poetry run nosetests
        
If tests don't pass in your environment, please check that dependencies match those described in pyproject.toml. One way to do it is to ensure that poetry runs commands in a dedicated virtualenv by setting environment variable as follow:

.. code:: bash

        poetry install --dev


Tests are provided with mocks, recorded with `VCR.py`_. In case you need
to (re)run tests, you should install the dataset in you PIM instance as
follow:

.. _Akeneo PIM API: https://api.akeneo.com/
.. _poetry: https://github.com/python-poetry/poetry
.. _VCR.py: http://vcrpy.readthedocs.io/en/latest/index.html
.. _pyproject.toml: https://python-poetry.org/docs/pyproject/

.. |Build Status| image:: https://travis-ci.org/matthieudelaro/akeneo_api_client.svg?branch=master
   :target: https://travis-ci.org/matthieudelaro/akeneo_api_client
.. |Documentation Status| image:: https://readthedocs.org/projects/akeneo-api-client/badge/?version=latest
   :target: http://akeneo-api-client.readthedocs.io/en/latest/
