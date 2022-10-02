from rest_framework import filters
import coreapi


class ProductFilters(filters.BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(name="status", location="query", required=False, type="string"),
            coreapi.Field(name="operation", location="query", required=False, type="string"),
        ]
