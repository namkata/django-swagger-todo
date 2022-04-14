from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from book.models import Book
from book.serializers import BookSerializer
from rest_framework.views import APIView

# from rest_framework.decorators import permission_classes

# Create your views here.

# # params books:
# params_books = openapi.Parameter('title', openapi.IN_QUERY,
#                                  description='The page in list books',
#                                  type=openapi.TYPE_STRING)
response_books = openapi.Response({
    'status': True,
    'message': None,
    'data': BookSerializer(many=True).data
})


@swagger_auto_schema(
    method='get',
    responses={status.HTTP_200_OK: response_books}
)
@api_view(['GET'])
def books(request: Request) -> Response:
    data = {
        "status": True,
        "message": None,
        "data": []
    }
    book = BookSerializer(many=True)
    data["data"] = book.data
    return Response(data=data, status=status.HTTP_200_OK)


class BookAPI(APIView):
    serializer_class = BookSerializer

    search_title_config = openapi.Parameter('title',
                                            openapi.IN_QUERY,
                                            description="Search title",
                                            type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[search_title_config],
                         responses={
                             status.HTTP_200_OK: BookSerializer(many=True)
                         })
    def get(self, request: Request) -> Response:
        title = request.GET.get('title', None)
        try:
            books = []
            if title:
                books = Book.objects.filter(title__icontains=title)

            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request: Request) -> Response:
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
