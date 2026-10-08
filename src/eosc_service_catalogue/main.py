"""
A trivial implementation of the EOSC Service Catalogue for a EGI Node
"""

from fastapi import FastAPI

from .base_router import create_router
from .eosc_service_catalogues_specs import catalogue_model_v1, catalogue_model_v2

# Create router with v1 model
v1_router = create_router(catalogue_model_v1, "v1")
v2_router = create_router(catalogue_model_v2, "v2")

app = FastAPI()
app.include_router(v1_router)
app.include_router(v1_router, prefix="/v1")
app.include_router(v2_router, prefix="/v2")
