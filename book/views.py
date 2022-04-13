from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request


# Create your views here.

@api_view(['GET'])
def books(request: Request) -> Response:
    data = {
        "status": True,
        "message": None,
        "data": []
    }
    return Response(data=data, status=status.HTTP_200_OK)
