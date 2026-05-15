"""
Tests to validate the catalogue data
"""

from importlib.resources import files

import yaml

from . import model


def test_validate_services_data():
    for svc_file in files("eosc_service_catalogue.data").iterdir():
        if not svc_file.name.endswith(".yaml"):
            continue
        print(f"Loading {svc_file}")
        svc = yaml.load(svc_file.read_text(), Loader=yaml.SafeLoader)
        assert model.EOSCServiceBundle.model_validate(svc)
