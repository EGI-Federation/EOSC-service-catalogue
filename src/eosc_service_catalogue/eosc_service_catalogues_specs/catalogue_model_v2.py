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
    """Service classification.

    publishing_discovery - Publishing & Discovery: Examples include catch-all
        repositories (e.g., Zenodo), data repositories (e.g., PANGAEA), software
        repositories, scientific data collections (e.g., Copernicus and biobanks),
        metadata aggregators and catalogues, scholarly knowledge graphs (SKGs),
        service catalogues, instrument registries, APIs, web portals, and semantic
        artefact catalogues (e.g., OntoPortal-based catalogues, EBI-based
        catalogues, and TIB Terminology Services).
    research_assessment_monitoring - Research Assessment & Monitoring: Examples
        include FAIR validators, Open Science monitoring tools, and research impact
        and evaluation systems.
    data_management_curation - Data Management & Curation: Examples include data
        management plan tools (DMP tools), metadata editors, curation and annotation
        platforms, and data policy management tools.
    data_processing_analysis - Data Processing & Analysis: Examples include Jupyter
        notebooks, workflow engines, analysis platforms, AI and machine-learning
        services, and statistical tools.
    compute_services - Compute Services: Examples include HPC clusters, cloud
        computing infrastructure (IaaS), virtual machines, and container
        orchestration platforms such as Kubernetes.
    storage_services - Storage Services: Examples include object storage such as S3,
        archival storage, file systems, backup services, long-term preservation
        platforms, and secure storage services.
    networking_services - Networking Services: Examples include research networks
        (NRENs), VPNs, high-speed data-transfer services, and federated connectivity
        services.
    science_gateways - Science Gateways: Examples include web-based research
        platforms, virtual laboratories, and Virtual Research Environments (VREs).
    instrumentation_physical_resources - Instrumentation & Physical Resources:
        Examples include laboratory instruments, sensors, IoT devices, and
        experimental facilities.
    research_support_collaboration - Research Support & Collaboration: Examples
        include user-support and consultancy services, collaboration platforms, and
        project-management tools.
    training_skills_development - Training & Skills Development: Examples include
        e-learning platforms, MOOCs, training portals, webinars, and certification
        services.
    infrastructure_operations_services - Infrastructure Operations Services:
        Examples include authentication and authorization infrastructures (AAI),
        federated identity systems such as eduGAIN, monitoring systems, and helpdesk
        platforms.
    persistent_identifiers - Persistent Identifiers: Examples include persistent
        identifier and registry services for researchers, organizations, and
        research resources, such as DOI, ORCID, and ROR.
    other - Other: Use this category if and only if the service does not match any
        of the other classifications.
    """

    publishing_discovery = 'service_classification-publishing_discovery'
    research_assessment_monitoring = 'service_classification-research_assessment_monitoring'
    data_management_curation = 'service_classification-data_management_curation'
    data_processing_analysis = 'service_classification-data_processing_analysis'
    compute_services = 'service_classification-compute_services'
    storage_services = 'service_classification-storage_services'
    networking_services = 'service_classification-networking_services'
    science_gateways = 'service_classification-science_gateways'
    instrumentation_physical_resources = 'service_classification-instrumentation_physical_resources'
    research_support_collaboration = 'service_classification-research_support_collaboration'
    training_skills_development = 'service_classification-training_skills_development'
    infrastructure_operations_services = 'service_classification-infrastructure_operations_services'
    persistent_identifiers = 'service_classification-persistent_identifiers'
    other = 'service_classification-other'


class ServiceCategory(BaseModel):
    category: Category = Field(
        description="Category of the service",
        examples=['service_classification-data_processing_analysis'])


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
