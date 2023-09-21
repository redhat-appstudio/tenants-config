"""Test the tenatns directories and manifests"""
from abc import abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import (
    Final,
    Iterable,
    Mapping,
    MutableMapping,
    NamedTuple,
    Protocol,
    Sequence,
)

import pytest
from pytest import Metafunc
from yaml import safe_load_all

TENANT_NAME: Final[str] = "tenant_name"
ALL_RESOURCES: Final[str] = "all_resources"


class ResourceViewer(Protocol):
    """Protocol for accessing the resource data

    A resource is a k8s object definition
    """

    @property
    @abstractmethod
    def data(self) -> Mapping:
        """The definition of the resource"""

    @property
    @abstractmethod
    def path(self) -> Path:
        """The path of the file the resource was loaded from"""


class ResourceWithContext(NamedTuple):
    """A resource and the path to its tenant's directory

    ctx: The path to the tenant's directory the resources belongs to
    resource: The resource
    """

    ctx: str
    resource: ResourceViewer


class TenantsViewer(Protocol):
    """Protocol for accessing Tenants data"""

    @property
    @abstractmethod
    def tenants_names(self) -> Iterable[str]:
        """Return the names of all the tenants"""

    @property
    @abstractmethod
    def resources_and_dirs(self) -> Iterable[ResourceWithContext]:
        """Returns all the resources with their context"""


@dataclass(frozen=True)
class Resource(ResourceViewer):
    """Resource implementation"""

    _data: Mapping
    _path: Path

    @property
    def data(self) -> Mapping:
        return self._data

    @property
    def path(self) -> Path:
        return self._path


@dataclass(frozen=True)
class TenantDir:
    """Represents a single tenant directory and its resources

    name: The name of the tenant (and its directory)
    resources: All the resources belong to the tenant
    """

    name: str
    resources: Sequence[ResourceViewer]


@dataclass(frozen=True)
class Tenants(TenantsViewer):
    """Tenants viewer implementation"""

    tenants: MutableMapping[str, TenantDir] = field(default_factory=dict)

    @property
    def tenants_names(self) -> Iterable[str]:
        return self.tenants.keys()

    @property
    def resources_and_dirs(self) -> Iterable[ResourceWithContext]:
        ret = []
        for tenant_dir in self.tenants.values():
            for res in tenant_dir.resources:
                ret.append(ResourceWithContext(tenant_dir.name, res))
        return ret


def load_tenants() -> TenantsViewer:
    """Loads all the tenants data from disk"""
    cur_file = Path(__file__)
    project_dir = cur_file.parent.parent
    cluster_dirs: Path = project_dir / "auto-generated/cluster"
    tenants = Tenants()
    for cluster_dir in filter(Path.is_dir, cluster_dirs.iterdir()):
        for subdir in filter(Path.is_dir, cluster_dir.iterdir()):
            for tenant_dir in subdir.iterdir():
                resources = list(tenant_dir.rglob("*"))
                filtered_resources = list(filter(Path.is_file, resources))
                loaded_resources = []
                for res_file in filtered_resources:
                    with res_file.open() as fil:
                        for data in safe_load_all(fil):
                            loaded_resources.append(
                                Resource(
                                    _data=data,
                                    _path=res_file,
                                )
                            )

                tenants.tenants[tenant_dir.name] = TenantDir(
                    name=tenant_dir.name, resources=loaded_resources
                )

    return tenants


TENANTS: Final[TenantsViewer] = load_tenants()


def pytest_generate_tests(metafunc: Metafunc) -> None:
    """Generate test parameters"""
    if TENANT_NAME in metafunc.fixturenames:
        parametrize_overlay(metafunc)
        return None
    if ALL_RESOURCES in metafunc.fixturenames:
        parametrize_resources(metafunc)
        return None

    return None


def parametrize_overlay(metafunc: Metafunc) -> None:
    """Generate parameters for each tenant name"""
    metafunc.parametrize(
        TENANT_NAME,
        TENANTS.tenants_names,
        ids=TENANTS.tenants_names,
        scope="module",
    )


def parametrize_resources(metafunc: Metafunc) -> None:
    """Generate parameters for reach tenants and its resources"""
    metafunc.parametrize(
        ALL_RESOURCES,
        TENANTS.resources_and_dirs,
        ids=(str(r.resource.path) for r in TENANTS.resources_and_dirs),
        scope="module",
    )


def test_tenant_name(tenant_name: str) -> None:
    """Verify the tenants name format"""
    assert tenant_name.endswith("-tenant")


def test_resource_namespace_matches_tenants_name(
    all_resources: tuple[str, ResourceViewer]
) -> None:
    """Verify the tenants doesn't try to deploy to other namespaces"""
    tenant_dir_name, resource = all_resources
    metadata = resource.data.get("metadata", {})
    namespace = metadata.get("namespace")
    if not namespace:
        pytest.fail("Namespace was not defined in the manifest")
    assert tenant_dir_name == namespace
