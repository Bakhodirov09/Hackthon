from django.urls import path, re_path
from apps.API.swagger.config import schema_view


urlpatterns = [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$', 
        schema_view.without_ui(cache_timeout = 0), 
        name = 'schema-json'
    ),
    path(
        '', 
        schema_view.with_ui('swagger', cache_timeout = 0), 
        name = 'schema-swagger-ui'
    ),
    path(
        'redoc/', 
        schema_view.with_ui('redoc', cache_timeout = 0), 
        name='schema-redoc'
    ),
]
