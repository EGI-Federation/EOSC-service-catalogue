"""
A trivial implementation of the EOSC Service Catalogue for a EGI Node
"""

from fastapi import FastAPI

from .base_router import create_router
from .eosc_service_catalogues_specs import catalogue_model_v1
from .eosc_service_catalogues_specs import catalogue_model_v2

# Create router with v1 model
v1_router = create_router(
    "v1",
    catalogue_model_v1.PagingServiceBundle,
    catalogue_model_v1.ServiceBundle,
    catalogue_model_v1.Service,
)
# Create router with v2 model
v2_router = create_router(
    "v2",
    catalogue_model_v2.PagingServiceBundle,
    catalogue_model_v2.ServiceBundle,
    catalogue_model_v2.Service,
)

app = FastAPI()
app.include_router(v1_router)
app.include_router(v1_router, prefix="/v1")
app.include_router(v2_router, prefix="/v2")
