from django.urls import path, include
from swagger_setting.swagger_schema import SwaggerSchemaView
# from rest_framework_swagger.views import get_swagger_view
# from django.conf import settings

# # Then import basically
# title = settings.SWAGGER_TITLE
# schema_view = get_swagger_view(title=title)
# can add more the url, parents, urlconf:
# eg: get_swagger_view(title="aaa", url="aaaa")

urlpatterns = [
    # path('', schema_view),
    path('', include("book.urls")),
    path('swagger/', SwaggerSchemaView.as_view())
]
