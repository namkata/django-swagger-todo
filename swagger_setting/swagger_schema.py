# **Create my swagger schema view by using a function based or class-based.

# import package
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.schemas import SchemaGenerator
from rest_framework_swagger import renderers


# class SwaggerShemaView - Class based view


class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)
        return Response(schema)

# ----------------------------------------#
# SwaggerSchemaView - function based view
# from rest_framework.decorators import api_view, renderer_classes
# from rest_framework import response, schemas
# from rest_framework_swagger.renderers import OpenAPIRenderer
# from rest_framework_swagger.renderers import SwaggerUIRenderer
# from django.conf import settings
# # That schema_view using SChemaGenerator do not customize
# @api_view(['GET'])
# @renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
# def schema_view(request):
#     generator = schemas.SchemaGenerator(title=settings.SWAGGER_TITLE)
#     return response.Response(generator.get_schema(request=request))
