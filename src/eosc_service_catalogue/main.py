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
from typing import Literal, Optional

import yaml
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

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


def keyword_filter(keyword: str):
    def check_keyword(svc: model.EoscServiceBundleSchemaV3):
        if any(keyword.casefold() in tag.casefold() for tag in svc.service.tags):
            return True
        return any(
            keyword.casefold() in (txt.casefold() if txt else "")
            for txt in (svc.service.name, svc.service.description, svc.service.tagline)
        )

    if not keyword:
        return lambda x: True
    else:
        return check_keyword


def service_sorter(sort_field: str = ""):
    def get_field(svc: model.EoscServiceBundleSchemaV3):
        return getattr(svc.service, sort_field)

    if not sort_field:
        sort_field = "id"
    return get_field


class ServicesResponse(BaseModel):
    total: int = Field(description="Total number of services")
    from_: int = Field(
        serialization_alias="from", description="Index of the first service returned"
    )
    to: int = Field(description="Index of the last service returned")
    results: list[model.EoscServiceBundleSchemaV3] = Field(description="Results")


@app.get("/services")
def services(
    keyword: Optional[str] = Query("", description="Keyword to refine the search"),
    from_: Optional[int] = Query(
        0,
        description="Starting index in the result set (default 0)",
        alias="from",
        ge=0,
    ),
    quantity: Optional[int] = Query(
        10, description="Quantity to be fetched (default 10)", ge=0
    ),
    order: Optional[Literal["asc", "desc"]] = Query(
        "asc", description="Order of results: 'asc' or 'desc' (default: 'asc')"
    ),
    sort_field: Optional[str] = Query(
        "", description="Field to user for ordering", alias="sort"
    ),
) -> ServicesResponse:
    """Get a list of Service profiles"""

    if sort_field and sort_field not in model.Service.model_fields.keys():
        raise HTTPException(
            status_code=400, detail=f"Invalid 'sort' field: {sort_field}"
        )

    # keyword filter
    # sort and filter by keyword
    bundle = sorted(
        filter(keyword_filter(keyword), load_services()), key=service_sorter(sort_field)
    )
    # return indexing as requested
    total = len(bundle)
    if from_ >= total:
        raise HTTPException(status_code=400, detail=f"Invalid 'from' value: {from_}")
    return ServicesResponse(
        total=total,
        from_=from_,
        to=min(from_ + quantity, total - 1),
        results=bundle[from_ : from_ + quantity],
    )
