"""
Tests for main.py application
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from ..main import app
from ..service_store import ServiceStore


def prefixed_services_endpoint_test(prefix):
    """Test the /services endpoint with various parameters"""
    client = TestClient(app)

    # Test basic endpoint call
    response = client.get(f"{prefix}/services")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "from" in data
    assert "to" in data
    assert "results" in data

    # Test with keyword filter
    response = client.get(f"{prefix}/services?keyword=compute")
    assert response.status_code == 200

    # Test with from parameter
    response = client.get(f"{prefix}/services?from=0")
    assert response.status_code == 200

    # Test with quantity parameter
    response = client.get(f"{prefix}/services?quantity=5")
    assert response.status_code == 200

    # Test with order parameter
    response = client.get(f"{prefix}/services?order=desc")
    assert response.status_code == 200

    # Test with sort parameter
    response = client.get(f"{prefix}/services?sort=name")
    assert response.status_code == 200

    # Test with invalid sort parameter (should return error)
    response = client.get(f"{prefix}/services?sort=invalid_field")
    assert response.status_code == 400

    # Test quantity and from parameters together
    response = client.get(f"{prefix}/services?from=0&quantity=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) <= 2

    # Test with quantity parameter
    response = client.get(f"{prefix}/services?quantity=-1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == data["total"]


def test_services_endpoints():
    prefixed_services_endpoint_test("")
    prefixed_services_endpoint_test("/v1")
    prefixed_services_endpoint_test("/v2")


def prefixed_services_endpoint_no_results_test(prefix):
    """Test the /services endpoint with various parameters"""
    client = TestClient(app)

    # Test basic endpoint call
    response = client.get(f"{prefix}/services?keyword=foobarinvalidfield")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["from"] == 0
    assert data["to"] == 0
    assert data["results"] == []


def test_services_endpoint_no_results():
    prefixed_services_endpoint_no_results_test("")
    prefixed_services_endpoint_no_results_test("/v1")
    prefixed_services_endpoint_no_results_test("/v2")


def prefixed_services_endpoint_with_data_test(prefix):
    """Test the service endpoint returns proper data structure"""
    client = TestClient(app)

    response = client.get(f"{prefix}/services")
    assert response.status_code == 200
    data = response.json()

    # Check response structure
    assert isinstance(data["total"], int)
    assert isinstance(data["from"], int)
    assert isinstance(data["to"], int)
    assert isinstance(data["results"], list)

    # Check that results contain valid service data
    if data["results"]:
        first_result = data["results"][0]
        assert "id" in first_result
        assert "service" in first_result
        service = first_result["service"]
        assert "id" in service
        assert "name" in service
        assert "webpage" in service
        assert "description" in service


def test_services_endpoint_with_data():
    prefixed_services_endpoint_with_data_test("")
    prefixed_services_endpoint_with_data_test("/v1")
    prefixed_services_endpoint_with_data_test("/v2")


def prefixed_404_service_test(prefix):
    client = TestClient(app)

    response = client.get(f"{prefix}/service/foo")
    assert response.status_code == 404


def test_404_service():
    prefixed_404_service_test("")
    prefixed_404_service_test("/v1")
    prefixed_404_service_test("/v2")


def prefixed_get_service_data(prefix, bundle):
    client = TestClient(app)

    with patch.object(ServiceStore, "load_services") as m_load:
        m_load.return_value = bundle
        response = client.get(f"{prefix}/service/test-id-1")
        assert response.status_code == 200
        assert response.json()["id"] == "test-id-1"


def test_get_service_data(bundle, bundle_v1):
    prefixed_get_service_data("", bundle_v1)
    prefixed_get_service_data("v1", bundle_v1)
    prefixed_get_service_data("v2", bundle)
