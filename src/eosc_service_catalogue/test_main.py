"""
Tests for main.py application
"""

from eosc_service_catalogue import model
from eosc_service_catalogue.main import (
    app,
    keyword_filter,
    load_services,
    mystrip,
    service_sorter,
)
from fastapi.testclient import TestClient


def test_load_services():
    """Test that services are loaded correctly"""
    services = load_services()
    assert isinstance(services, list)
    assert len(services) > 0
    # Check that at least one service is valid
    sample = services[0]
    assert hasattr(sample, "service")
    assert hasattr(sample.service, "id")
    assert hasattr(sample.service, "name")


def test_keyword_filter():
    """Test keyword filtering functionality"""
    # Create a mock service bundle
    mock_service = model.EOSCServiceBundle(
        id="test-id",
        service=model.Service(
            id="test-id",
            name="Test Service",
            webpage="https://example.com",
            description="This is a test service",
            tagline="Test tagline",
            scientificDomains=[
                model.ScientificDomainEntry(
                    scientificDomain=model.ScientificDomains.scientific_domain_generic
                )
            ],
            categories=[
                model.ServiceCategoryEntry(
                    category=model.CategoryId.category_other_other
                )
            ],
            targetUsers=[model.TargetUser.target_user_researchers],
            languageAvailabilities=[model.LanguageCode.en],
            trl=model.TRL.trl_1,
            orderType=model.OrderType.order_type_other,
            tags=[],
        ),
    )

    # Test no keyword (should return True for all)
    filter_func = keyword_filter(None)
    assert filter_func(mock_service) is True

    # Test empty keyword (should return True for all)
    filter_func = keyword_filter("")
    assert filter_func(mock_service) is True

    # Test matching keyword in name
    filter_func = keyword_filter("Test")
    assert filter_func(mock_service) is True

    # Test non-matching keyword
    filter_func = keyword_filter("Nonexistent")
    assert filter_func(mock_service) is False


def test_service_sorter():
    """Test service sorting functionality"""
    # Create mock services
    svc1 = model.EOSCServiceBundle(
        id="test-id-1",
        service=model.Service(
            id="test-id-1",
            name="A Service",
            webpage="https://example.com",
            description="Test description",
            tagline="Test tagline",
            scientificDomains=[
                model.ScientificDomainEntry(
                    scientificDomain=model.ScientificDomains.scientific_domain_generic
                )
            ],
            categories=[
                model.ServiceCategoryEntry(
                    category=model.CategoryId.category_other_other
                )
            ],
            targetUsers=[model.TargetUser.target_user_researchers],
            languageAvailabilities=[model.LanguageCode.en],
            trl=model.TRL.trl_1,
            orderType=model.OrderType.order_type_other,
            tags=[],
        ),
    )

    svc2 = model.EOSCServiceBundle(
        id="test-id-2",
        service=model.Service(
            id="test-id-2",
            name="B Service",
            webpage="https://example.com",
            description="Test description",
            tagline="Test tagline",
            scientificDomains=[
                model.ScientificDomainEntry(
                    scientificDomain=model.ScientificDomains.scientific_domain_generic
                )
            ],
            categories=[
                model.ServiceCategoryEntry(
                    category=model.CategoryId.category_other_other
                )
            ],
            targetUsers=[model.TargetUser.target_user_researchers],
            languageAvailabilities=[model.LanguageCode.en],
            trl=model.TRL.trl_1,
            orderType=model.OrderType.order_type_other,
            tags=[],
        ),
    )

    # Test default sorting (by id)
    sorter = service_sorter("")
    assert sorter(svc1) == "test-id-1"
    assert sorter(svc2) == "test-id-2"

    # Test explicit sorting by name
    sorter = service_sorter("name")
    assert sorter(svc1) == "A Service"
    assert sorter(svc2) == "B Service"


def test_services_endpoint():
    """Test the /services endpoint with various parameters"""
    client = TestClient(app)

    # Test basic endpoint call
    response = client.get("/services")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "from" in data
    assert "to" in data
    assert "results" in data

    # Test with keyword filter
    response = client.get("/services?keyword=compute")
    assert response.status_code == 200

    # Test with from parameter
    response = client.get("/services?from=0")
    assert response.status_code == 200

    # Test with quantity parameter
    response = client.get("/services?quantity=5")
    assert response.status_code == 200

    # Test with order parameter
    response = client.get("/services?order=desc")
    assert response.status_code == 200

    # Test with sort parameter
    response = client.get("/services?sort=name")
    assert response.status_code == 200

    # Test with invalid sort parameter (should return error)
    response = client.get("/services?sort=invalid_field")
    assert response.status_code == 400

    # Test quantity and from parameters together
    response = client.get("/services?from=0&quantity=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) <= 2

    # Test with quantity parameter
    response = client.get("/services?quantity=-1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == data["total"]


def test_services_endpoint_no_results():
    """Test the /services endpoint with various parameters"""
    client = TestClient(app)

    # Test basic endpoint call
    response = client.get("/services?keyword=foobarinvalidfield")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["from"] == 0
    assert data["to"] == 0
    assert data["results"] == []


def test_services_endpoint_with_data():
    """Test the service endpoint returns proper data structure"""
    client = TestClient(app)

    response = client.get("/services")
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


def test_mystrip_function():
    """Test the mystrip helper function"""
    # Test normal text - based on actual implementation of mystrip
    result = mystrip("hello\nworld")
    expected = "helloworld"  # mystrip strips newlines and joins content
    assert result == expected

    # Test with extra whitespace
    result = mystrip("  hello  \n  world  ")
    expected = "helloworld"  # mystrip strips each line completely via strip()
    assert result == expected

    # Test empty string (behavior is to return '\n' due to split behavior)
    result = mystrip("")
    expected = "\n"
    assert result == expected
