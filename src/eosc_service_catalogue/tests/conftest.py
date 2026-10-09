import pytest

from ..eosc_service_catalogues_specs import catalogue_model_v1
from ..eosc_service_catalogues_specs import catalogue_model_v2 as model


@pytest.fixture
def mock_service():
    return model.ServiceBundle(
        id="test-id-1",
        service=model.Service(
            id="test-id-1",
            name="B Service",
            webpage="https://example.com",
            description="Test description",
            tagline="Test tagline",
            scientificDomains=[
                model.ServiceProviderDomain(
                    scientificDomain=model.ScientificDomain.generic
                )
            ],
            categories=[model.ServiceCategory(category=model.Category.other)],
            targetUsers=[model.TargetUser.researchers],
            languageAvailabilities=["en"],
            trl=model.TRL.trl_1,
            orderType=model.OrderType.other,
            tags=["tag-foo"],
        ),
    )


@pytest.fixture
def mock_service_2():
    return model.ServiceBundle(
        id="test-id-2",
        service=model.Service(
            id="test-id-2",
            name="A Service",
            webpage="https://example.com",
            description="Test description",
            tagline="Test tagline",
            scientificDomains=[
                model.ServiceProviderDomain(
                    scientificDomain=model.ScientificDomain.generic
                )
            ],
            categories=[model.ServiceCategory(category=model.Category.other)],
            targetUsers=[model.TargetUser.researchers],
            languageAvailabilities=["en"],
            trl=model.TRL.trl_1,
            orderType=model.OrderType.other,
            tags=[],
        ),
    )


@pytest.fixture
def bundle(mock_service, mock_service_2):
    return {mock_service.id: mock_service, mock_service_2.id: mock_service_2}


@pytest.fixture
def mock_service_v1():
    return catalogue_model_v1.ServiceBundle(
        id="test-id-1",
        service=catalogue_model_v1.Service(
            id="test-id-1",
            name="B Service",
            webpage="https://example.com",
            description="Test description",
            tagline="Test tagline",
            scientificDomains=[
                catalogue_model_v1.ServiceProviderDomain(
                    scientificDomain=catalogue_model_v1.ScientificDomain.generic
                )
            ],
            categories=[
                catalogue_model_v1.ServiceCategory(
                    category=catalogue_model_v1.Category.other_other
                )
            ],
            targetUsers=[catalogue_model_v1.TargetUser.researchers],
            languageAvailabilities=["en"],
            trl=catalogue_model_v1.TRL.trl_1,
            orderType=catalogue_model_v1.OrderType.other,
            tags=["tag-foo"],
        ),
    )


@pytest.fixture
def mock_service_2_v2():
    return catalogue_model_v1.ServiceBundle(
        id="test-id-2",
        service=catalogue_model_v1.Service(
            id="test-id-2",
            name="A Service",
            webpage="https://example.com",
            description="Test description",
            tagline="Test tagline",
            scientificDomains=[
                catalogue_model_v1.ServiceProviderDomain(
                    scientificDomain=catalogue_model_v1.ScientificDomain.generic
                )
            ],
            categories=[
                catalogue_model_v1.ServiceCategory(
                    category=catalogue_model_v1.Category.processing_and_analysis_data_analysis
                )
            ],
            targetUsers=[catalogue_model_v1.TargetUser.resource_managers],
            languageAvailabilities=["en"],
            trl=catalogue_model_v1.TRL.trl_1,
            orderType=catalogue_model_v1.OrderType.other,
            tags=[],
        ),
    )


@pytest.fixture
def bundle_v1(mock_service_v1, mock_service_2_v2):
    return {
        mock_service_v1.id: mock_service_v1,
        mock_service_2_v2.id: mock_service_2_v2,
    }
