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

from fastapi import FastAPI
from enum import Enum

from pydantic_core import from_json

import yaml

app = FastAPI()


from importlib.resources import files

from . import model


def load_services() -> list[model.EoscServiceBundleSchemaV3]:
    services = []
    for svc_file in files("eosc_service_catalogue.data").iterdir():
        try:
            svc = yaml.load(svc_file.read_text(), Loader=yaml.SafeLoader)
            services.append(model.EoscServiceBundleSchemaV3.model_validate(svc))
        except Exception as e:
            print(e)
            continue
    return services


class OrderEnum(str, Enum):
    asc = "asc"
    desc = "desc"


@app.get("/services")
def services(
    keyword: str | None = None,
    from_change_me: int | None = 0,
    quantity: int | None = 10,
    order: OrderEnum | None = "asc",
    sort: str | None = None,
) -> list[model.EoscServiceBundleSchemaV3]:
    """Get a list of Service profiles based on a set of filters.

    Params:
    - keyword: String (Keyword to refine the search) [optional]
    - from: String (Starting index in the result set, default 0) [optional]
    - quantity: String (Quantity to be fetched, default 10) [optional]
    - order: String (Order of results - asc/desc, default asc) [optional]
    - sort: String (Field to use for ordering) [optional
    """
    return load_services()
