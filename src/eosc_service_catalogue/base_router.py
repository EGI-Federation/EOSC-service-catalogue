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

from typing import Literal, Type

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from . import service_store


def create_router(
    version: str,
    model_response: Type[BaseModel],
    model_bundle: Type[BaseModel],
    svc_class: Type[BaseModel],
) -> APIRouter:
    """Create a router instance with specific model class"""
    router = APIRouter()
    svc_store = service_store.ServiceStore(model_bundle, version)

    @router.get("/services", response_model=model_response)
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

        service_fields = svc_class.model_fields
        if sort_field and sort_field not in service_fields:
            raise HTTPException(
                status_code=400, detail=f"Invalid 'sort' field: {sort_field}"
            )

        # keyword filter
        # sort and filter by keyword
        bundle = svc_store.filtered_services(keyword, sort_field, order == "desc")
        total = len(bundle)
        if not total:
            return model_response(
                total=0,
                from_=0,
                to=0,
                results=[],
            )
        start = from_ if from_ else 0
        if quantity is None:
            quantity = -1
        quantity = quantity if quantity != -1 else total
        end = min(start + quantity, total) if start < total else start
        return model_response(
            total=total,
            from_=start,
            to=end,
            results=bundle[start:end],
        )

    @router.get("/service/{service_id}", response_model=model_bundle)
    def service(service_id: str):
        """Get a single service"""
        svc = svc_store.get_service(service_id)
        if not svc:
            raise HTTPException(
                status_code=404, detail=f"Service {service_id} not found"
            )
        return svc

    return router
