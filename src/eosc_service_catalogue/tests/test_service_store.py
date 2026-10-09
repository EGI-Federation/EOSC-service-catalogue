"""
Tests to validate service store
"""

from importlib.resources import files

from .. import service_store
from ..eosc_service_catalogues_specs import catalogue_model_v1
from ..eosc_service_catalogues_specs import catalogue_model_v2 as model


def test_validate_services_data():
    files_count = len(
        [
            f
            for f in files("eosc_service_catalogue.data").iterdir()
            if f.name.endswith(".yaml")
        ]
    )
    versions = [
        (catalogue_model_v1.ServiceBundle, "v1"),
        (model.ServiceBundle, "v2"),
    ]
    for m, v in versions:
        ss = service_store.ServiceStore(m, v)
        ss.load_services()
        assert len(ss.bundle) == files_count


def test_keyword_filter(mock_service):
    """Test keyword filtering functionality"""
    # Test no keyword (should return True for all)
    filter_func = service_store._keyword_filter(None)
    assert filter_func(mock_service) is True

    # Test empty keyword (should return True for all)
    filter_func = service_store._keyword_filter("")
    assert filter_func(mock_service) is True

    # Test matching keyword in name
    filter_func = service_store._keyword_filter("Test")
    assert filter_func(mock_service) is True

    # Test matching keyword in tag
    filter_func = service_store._keyword_filter("tag-foo")
    assert filter_func(mock_service) is True

    # Test non-matching keyword
    filter_func = service_store._keyword_filter("Nonexistent")
    assert filter_func(mock_service) is False


def test_service_sorter(mock_service, mock_service_2):
    """Test service sorting functionality"""

    # Test default sorting (by id)
    sorter = service_store._service_sorter("")
    assert sorter(mock_service) == "test-id-1"
    assert sorter(mock_service_2) == "test-id-2"

    # Test explicit sorting by name
    sorter = service_store._service_sorter("name")
    assert sorter(mock_service) == "B Service"
    assert sorter(mock_service_2) == "A Service"


def test_service_get(bundle):
    ss = service_store.ServiceStore(model.ServiceBundle, "v2")
    # mock the internal bundle
    ss.bundle = bundle

    assert ss.get_service("test-id-1") == bundle.get("test-id-1")
    assert ss.get_service("non-existent") is None


def test_filtered_services(bundle):
    ss = service_store.ServiceStore(model.ServiceBundle, "v2")
    # mock the internal bundle
    ss.bundle = bundle

    assert [s.id for s in ss.filtered_services("", "", False)] == [
        "test-id-1",
        "test-id-2",
    ]
    assert [s.id for s in ss.filtered_services("", "", True)] == [
        "test-id-2",
        "test-id-1",
    ]
    assert [s.id for s in ss.filtered_services("B Service", "", False)] == ["test-id-1"]
    assert [s.id for s in ss.filtered_services("", "name", False)] == [
        "test-id-2",
        "test-id-1",
    ]
