"""
A trivial implementation of the EOSC Service Catalogue for a EGI Node

Follows specification at https://zenodo.org/records/18622838

The API of the service catalogue must implement one method
/services //Get a list of Service profiles based on a set of filters.
Params:
- keyword: String (Keyword to refine the search) [optional]
- from: String (Starting index in the result set, default 0) [optional]
- quantity: String (Quantity to be fetched, default 10) [optional]
- order: String (Order of results - asc/desc, default asc) [optional]
- sort: String (Field to use for ordering) [optional
"""

from importlib.resources import files

import yaml
from fastapi import FastAPI

from . import model

app = FastAPI()

_egi_service_bundle: list[model.EoscServiceBundleSchemaV3] = []


def load_services() -> list[model.EoscServiceBundleSchemaV3]:
    """Loads the services from the data files"""
    global _egi_service_bundle
    if not _egi_service_bundle:
        for svc_file in files("eosc_service_catalogue.data").iterdir():
            if not svc_file.name.endswith(".yaml"):
                continue
            try:
                svc = yaml.load(svc_file.read_text(), Loader=yaml.SafeLoader)
                _egi_service_bundle.append(
                    model.EoscServiceBundleSchemaV3.model_validate(svc)
                )
            except Exception as e:
                print(e)
                continue
    return _egi_service_bundle


@app.get("/services")
def services() -> list[model.EoscServiceBundleSchemaV3]:
    """Get a list of Service profiles"""
    return load_services()
