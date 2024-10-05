""" Swagger documentation urls """

# Django
from django.urls import path

# Drf Yasg
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_yasg.generators import OpenAPISchemaGenerator


class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, *args, **kwargs):
        schema = super().get_schema(*args, **kwargs)

        schema.tags = [{"name": "pokedex"}]

        schema["x-tagGroups"] = [
            {
                "name": "Pokedex",
                "tags": ["pokedex"],
            }
        ]

        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="API OAK",
        default_version="1.0.0",
        description="After years of work, Professor oak has realeased his pokemon's investigation."
        + "This API provides you of basic information of pokemon world",
    ),
    public=True,
    generator_class=CustomSchemaGenerator,
)

docs_endpoint = [
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
