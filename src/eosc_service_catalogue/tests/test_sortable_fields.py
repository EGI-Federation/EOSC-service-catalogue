"""
Tests for the _sortable_fields function
"""

from pydantic import BaseModel

from ..base_router import _sortable_fields


class SimpleModel(BaseModel):
    name: str
    age: int
    active: bool
    score: float
    non_scalar: list


class ComplexModel(BaseModel):
    id: str
    title: str
    count: int
    is_published: bool
    rating: float | None = None
    tags: list | None = None


def test_sortable_fields_simple_model():
    """Test sortable fields extraction from a simple model"""
    fields = _sortable_fields(SimpleModel)

    # Should contain all scalar fields
    expected_fields = {"name", "age", "active", "score"}
    assert fields == expected_fields


def test_sortable_fields_complex_model():
    """Test sortable fields extraction from a complex model"""
    fields = _sortable_fields(ComplexModel)

    # Should contain all scalar fields (Optional fields should be included if their type is scalar)
    expected_fields = {"id", "title", "count", "is_published", "rating"}
    assert fields == expected_fields


def test_sortable_fields_with_optional_fields():
    """Test sortable fields with optional scalar field types"""

    class OptionalModel(BaseModel):
        name: str
        age: int | None = None
        active: bool | None = False
        score: float | None = 0.0
        description: str | None = None

    fields = _sortable_fields(OptionalModel)

    # Should include all scalar fields, including optional ones
    expected_fields = {"name", "age", "active", "score", "description"}
    assert fields == expected_fields


def test_sortable_fields_with_non_scalar_fields():
    """Test sortable fields with non-scalar field types"""

    class MixedModel(BaseModel):
        name: str
        age: int
        nested_object: dict  # Non-scalar field - should be excluded
        list_field: list  # Non-scalar field - should be excluded
        optional_list: list | None = None  # Non-scalar field - should be excluded

    fields = _sortable_fields(MixedModel)

    # Should only include scalar field types
    expected_fields = {"name", "age"}
    assert fields == expected_fields


def test_sortable_fields_empty_model():
    """Test sortable fields with no scalar fields"""

    class EmptyModel(BaseModel):
        nested_dict: dict
        list_field: list

    fields = _sortable_fields(EmptyModel)

    # Should return empty set
    assert fields == set()


def test_sortable_fields_no_fields():
    """Test sortable fields with no fields at all"""

    class NoFieldsModel(BaseModel):
        pass

    fields = _sortable_fields(NoFieldsModel)

    # Should return empty set
    assert fields == set()
