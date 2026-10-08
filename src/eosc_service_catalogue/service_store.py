"""The Service Store keeps the service data ready for the API"""

from importlib.resources import files
import re

import yaml

VERSION_SUFFIX_RE = r"(.*)__(.*)$"

def _keyword_filter(keyword: str | None):
    if not keyword:
        return lambda x: True

    def check_keyword(svc):
        if svc.service.tags and any(
            keyword.casefold() in tag.casefold() for tag in svc.service.tags
        ):
            return True
        return any(
            keyword.casefold() in (txt.casefold() if txt else "")
            for txt in (svc.service.name, svc.service.description, svc.service.tagline)
        )

    return check_keyword


def _service_sorter(sort_field: str | None = ""):
    if not sort_field:
        sort_field = "id"

    def get_field(svc):
        return getattr(svc.service, sort_field)

    return get_field


class ServiceStore:
    def __init__(self, service_class: type, version: str = "v1"):
        self.bundle = {}
        self.service_class = service_class
        self.version= version

    def load_services(self) -> dict:
        """Loads the services from the data files"""
        if not self.bundle:
            for svc_file in files("eosc_service_catalogue.data").iterdir():
                if not svc_file.name.endswith(".yaml"):
                    continue
                try:
                    svc_yaml = yaml.load(svc_file.read_text(), Loader=yaml.SafeLoader)
                    # handle different versions of the data, we need to be aware of the
                    # inner structure and find fields ending with __some_version_string
                    service = svc_yaml.get("service", {})
                    updated_fields = {}
                    fields_to_remove = []
                    for field in service: 
                        m = re.match(VERSION_SUFFIX_RE, field)
                        if m:
                            if m.groups()[1] == self.version:
                                updated_fields[m.groups()[0]] = service[field]
                            fields_to_remove.append(field)
                    service.update(updated_fields)
                    for field in fields_to_remove:
                        service.pop(field)
                    svc = self.service_class.model_validate(svc_yaml)
                    self.bundle[svc.id] = svc
                except Exception as e:
                    print(f"Error processing {svc_file}: {e}")
                    continue
        return self.bundle

    def filtered_services(
        self, keyword: str, sort_field: str, reverse: bool = False
    ) -> list:
        """Returns the service bundle list filtered by keyword and sorted by a given field"""
        return sorted(
            filter(_keyword_filter(keyword), list(self.load_services().values())),
            key=_service_sorter(sort_field),
            reverse=reverse,
        )

    def get_service(self, service_id: str):
        """gets a service by id"""
        return self.load_services().get(service_id, None)
