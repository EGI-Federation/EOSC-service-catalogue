from __future__ import annotations

from enum import Enum
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class HTTPError(BaseModel):
    detail: str


class PagingServiceBundle(BaseModel):
    total: int = Field(
        0,
        description='Total number of results matching the search criteria')
    from_: int = Field(
        0,
        alias='from',
        description="The index of the first element in results. It's inclusive and zero based")
    to: int = Field(
        0,
        description="The index of element after the last in results")
    results: Optional[List[ServiceBundle]] = None


class ServiceBundle(BaseModel):
    id: str = Field(description='Unique identifier for the service', examples=['surf-node:servicebundle:123456'])
    service: Service = Field(
        description='Metadata of the actual resource')


class Service(BaseModel):
    id: str = Field(
        description='Unique identifier for the service (use the same value as the Service Bundle ID)',
        examples=['surf-node:servicebundle:123456'])
    alternativeIdentifiers: Optional[List[AlternativeIdentifier]] = Field(
        None,
        description="List of alternative identifiers for the service",
        examples=[[{"type": "doi", "value": "10.1234/example.svc.123456"}]])
    abbreviation: Optional[str] = Field(
        None,
        description="Abbreviation of the service's name.",
        examples=['EXSVC'])
    name: str = Field(
        description="Full name of the service",
        examples=['Example Service for Research Data Processing'])
    webpage: str = Field(
        description="URL of the service's webpage",
        examples=['https://service.example.org'])
    description: str = Field(
        description="An abstract with a detailed description of the service",
        examples=[
            'Example Service for Research Data Processing provides scalable compute, curated datasets, and workflows to support reproducible research across multiple scientific domains.'])
    tagline: Optional[str] = Field(
        None,
        description="Short tagline summarizing the service",
        examples=['Scalable, reproducible research processing'])
    logo: Optional[str] = Field(
        None,
        description="URL of the service's logo",
        examples=['https://service.example.org/assets/logo.png'])
    scientificDomains: List[ServiceProviderDomain] = Field(
        description="List of scientific domains related to the service")
    categories: List[ServiceCategory] = Field(
        description="Categories the service, i.e., type of service")
    targetUsers: List[TargetUser] = Field(
        description="List of target users for the service")
    accessModes: Optional[List[AccessMode]] = Field(
        None,
        description="Types of access provided by the service")
    tags: Optional[List[str]] = Field(
        None,
        description="Tags associated with the service",
        examples=[['Reproducibility', 'workflows', 'datasets', 'high-performance']])
    languageAvailabilities: List[str] = Field(
        description="List of language availabilities of the service  (ISO 639-1 Code)",
        examples=[["en", "nl"]])
    helpdeskEmail: Optional[str] = Field(
        None,
        description="Email address for the service's helpdesk",
        examples=['helpdesk@example.org'])
    securityContactEmail: Optional[str] = Field(
        None,
        description="Email address for security contact",
        examples=['security@example.org'])
    trl: TRL = Field(
        description="Technology Readiness Level of the service")
    userManual: Optional[str] = Field(
        None,
        description="URL of the user manual",
        examples=['https://service.example.org/docs'])
    termsOfUse: Optional[str] = Field(
        None,
        description="URL of the terms of use",
        examples=['https://service.example.org/legal/terms'])
    privacyPolicy: Optional[str] = Field(
        None,
        description="URL of the privacy policy",
        examples=['https://service.example.org/legal/privacy'])
    accessPolicy: Optional[str] = Field(
        None,
        description="URL of the access policy",
        examples=['https://service.example.org/legal/access'])
    orderType: OrderType = Field(
        description="Service access modality")


class AlternativeIdentifier(BaseModel):
    type: Optional[str] = Field(
        None,
        description="Type of the alternative identifier",
        examples=['Any of OpenDOAR, re3data, handle, doi, FAIRSharing'])
    value: Optional[str] = Field(
        None,
        description="Value of the alternative identifier",
        examples=[
            '10.1234/example.svc.123456, 21.1234/EX-SVC-123456 When using PIDs for instruments https://docs.pidinst.org/en/latest/'])


class ScientificDomain(Enum):
    agricultural_sciences = 'scientific_domain-agricultural_sciences'
    engineering_and_technology = 'scientific_domain-engineering_and_technology'
    generic = 'scientific_domain-generic'
    humanities = 'scientific_domain-humanities'
    medical_and_health_sciences = 'scientific_domain-medical_and_health_sciences'
    natural_sciences = 'scientific_domain-natural_sciences'
    other = 'scientific_domain-other'
    social_sciences = 'scientific_domain-social_sciences'


class ServiceProviderDomain(BaseModel):
    scientificDomain: ScientificDomain = Field(
        description="Scientific domain related to the catalogue",
        examples=['scientific_domain-social_sciences'])


class Category(Enum):
    # Physical and e-Infrastructure Access
    access_physical_and_einfrastructure_compute = 'category-access_physical_and_eInfrastructures-compute'
    access_physical_and_einfrastructure_data_storage = 'category-access_physical_and_eInfrastructures-data_storage'
    access_physical_and_einfrastructure_instrument_and_equipment = 'category-access_physical_and_eInfrastructures-instrument_and_equipment'
    access_physical_and_einfrastructure_material_storage = 'category-access_physical_and_eInfrastructures-material_storage'
    access_physical_and_einfrastructure_network = 'category-access_physical_and_eInfrastructures-network'

    # Aggregators and Integrators
    aggregators_and_integrators_aggregators_and_integrators = 'category-aggregators_and_integrators-aggregators_and_integrators'

    # Other
    other_other = 'category-other-other'

    # Processing and Analysis
    processing_and_analysis_data_analysis = 'category-processing_and_analysis-data_analysis'
    processing_and_analysis_data_management = 'category-processing_and_analysis-data_management'
    processing_and_analysis_measurement_and_materials_analysis = 'category-processing_and_analysis-measurement_and_materials_analysis'

    # Security and Operations
    security_and_operations_operations_and_infrastructure_management_services = 'category-security_and_operations-operations_and_infrastructure_management_services'
    security_and_operations_security_and_identity = 'category-security_and_operations-security_and_identity'

    # Sharing and Discovery
    sharing_and_discovery_applications = 'category-sharing_and_discovery-applications'
    sharing_and_discovery_data = 'category-sharing_and_discovery-data'
    sharing_and_discovery_development_resources = 'category-sharing_and_discovery-development_resources'
    sharing_and_discovery_samples = 'category-sharing_and_discovery-samples'
    sharing_and_discovery_scholarly_communication = 'category-sharing_and_discovery-scholarly_communication'
    sharing_and_discovery_software = 'category-sharing_and_discovery-software'

    # Training and Support
    training_and_support_consultancy_and_support = 'category-training_and_support-consultancy_and_support'
    training_and_support_education_and_training = 'category-training_and_support-education_and_training'


class ServiceCategory(BaseModel):
    category: Category = Field(
        description="Category of the service",
        examples=['category-processing_and_analysis-data_analysis'])


class TargetUser(Enum):
    businesses = 'target_user-businesses'
    eu_node_users = 'target_user-eu_node_users'
    funders = 'target_user-funders'
    innovators = 'target_user-innovators'
    other = 'target_user-other'
    policy_makers = 'target_user-policy_makers'
    providers = 'target_user-providers'
    publishers = 'target_user-publishers'
    research_communities = 'target_user-research_communities'
    research_groups = 'target_user-research_groups'
    research_infrastructure_managers = 'target_user-research_infrastructure_managers'
    research_managers = 'target_user-research_managers'
    research_networks = 'target_user-research_networks'
    research_organisations = 'target_user-research_organisations'
    research_projects = 'target_user-research_projects'
    researchers = 'target_user-researchers'
    resource_managers = 'target_user-resource_managers'
    resource_provider_managers = 'target_user-resource_provider_managers'
    students = 'target_user-students'


class AccessMode(Enum):
    free = 'access_mode-free'
    free_conditionally = 'access_mode-free_conditionally'
    other = 'access_mode-other'
    paid = 'access_mode-paid'
    peer_reviewed = 'access_mode-peer_reviewed'


class TRL(Enum):
    trl_1 = 'trl-1'
    trl_2 = 'trl-2'
    trl_3 = 'trl-3'
    trl_4 = 'trl-4'
    trl_5 = 'trl-5'
    trl_6 = 'trl-6'
    trl_7 = 'trl-7'
    trl_8 = 'trl-8'
    trl_9 = 'trl-9'


class OrderType(Enum):
    fully_open_access = 'order_type-fully_open_access'
    open_access = 'order_type-open_access'
    order_required = 'order_type-order_required'
    other = 'order_type-other'
