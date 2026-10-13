"""
Base router for APIs that just diverge in the underlying service model

Follows specification at https://zenodo.org/records/18622838

The API of the service catalogue must implement one method
/services //Get a list of Service profiles based on a set of filters.
Params:
- keyword: String (Keyword to refine the search) [optional]
- from: String (Starting index in the result set, default 0) [optional]
- quantity: String (Quantity to be fetched, default 10) [optional]
- order: String (Order of results - asc/desc, default asc) [optional]
- sort: String (Field to use for ordering) [optional


We add an additional getter for a single service
/service/{service_id} // Get a service by its id
"""

from typing import Literal, Optional, get_args, get_origin

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from . import service_store


def create_router(
    version: str,
    response_class: type[BaseModel],
    bundle_class: type[BaseModel],
    svc_class: type[BaseModel],
) -> APIRouter:
    """Create a router instance with specific model class"""
    router = APIRouter()
    svc_store = service_store.ServiceStore(bundle_class, version)

    # Dynamically determine allowed scalar fields for sorting from the service model
    allowed_sort_fields = set()

    for field_name, field_info in svc_class.model_fields.items():
        field_type = field_info.annotation
        if field_type is not None:
            # Handle different types of field annotations
            origin = get_origin(field_type)

            # If type has no origin or is a basic scalar type
            if origin is None:
                if field_type in (str, int, float, bool):
                    allowed_sort_fields.add(field_name)
            # Handle Optional[type] - check the inner type
            elif origin == Optional:
                args = get_args(field_type)
                for arg in args:
                    if arg is not type(None):  # Skip None type
                        if arg in (str, int, float, bool):
                            allowed_sort_fields.add(field_name)
                        break  # Only consider first non-None argument

    @router.get("/services", response_model=response_class)
    def services(
        keyword: str | None = Query("", description="Keyword to refine the search"),
        from_: int | None = Query(
            0,
            description="Starting index in the result set (default 0)",
            alias="from",
            ge=0,
        ),
        quantity: int | None = Query(
            -1,
            description="Quantity to be fetched, -1 gets all records (default -1)",
            ge=-1,
        ),
        order: Literal["asc", "desc"] | None = Query(
            "asc", description="Order of results: 'asc' or 'desc' (default: 'asc')"
        ),
        sort_field: str | None = Query(
            "", description="Field to user for ordering", alias="sort"
        ),
    ):
        """Get a list of Service profiles"""

        # Check if sort_field is allowed
        if sort_field and sort_field not in allowed_sort_fields:
            raise HTTPException(
                status_code=400, detail=f"Invalid 'sort' field: {sort_field}"
            )

        # keyword filter
        # sort and filter by keyword
        bundle = svc_store.filtered_services(keyword, sort_field, order == "desc")
        total = len(bundle)
        if not total:
            return response_class(
                # using this to avoid "from" as it's reserved in python
                **{
                    "total": 0,
                    "from_": 0,
                    "to": 0,
                    "results": [],
                }
            )
        start = from_ if from_ else 0
        quantity = quantity if quantity != -1 else total
        end = min(start + quantity, total) if start < total else start
        return response_class(
            # using this to avoid "from" as it's reserved in python
            **{
                "total": total,
                "from": start,
                "to": end,
                "results": bundle[start:end],
            }
        )

    @router.get("/service/{service_id}", response_model=bundle_class)
    def service(service_id: str):
        """Get a single service"""
        svc = svc_store.get_service(service_id)
        if not svc:
            raise HTTPException(
                status_code=404, detail=f"Service {service_id} not found"
            )
        return svc

    return router
