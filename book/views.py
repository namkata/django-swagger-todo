from django.http import Http404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from book.models import Book
from book.serializers import BookSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import permission_classes
# from rest_framework.decorators import api_view


class BookAPI(APIView):
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)
    search_title_config = openapi.Parameter('title',
                                            openapi.IN_QUERY,
                                            description="Search title",
                                            type=openapi.TYPE_STRING)

    @swagger_auto_schema(
        method='get',
        operation_description="List all books",
        manual_parameters=[search_title_config],
        responses={
            status.HTTP_200_OK: BookSerializer(many=True)
        })
    # can use @action(methods=['GET'], detail=False) or @api_view(['GET'])
    @action(methods=['GET'], detail=False)
    def get(self, request: Request) -> Response:
        title = request.GET.get('title', None)
        try:
            list_book = Book.objects.all()
            if title:
                list_book = list_book.filter(title__icontains=title)

            serializer = BookSerializer(list_book, many=True)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    book_bodies = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['title', 'desc'],
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING),
            'desc': openapi.Schema(type=openapi.TYPE_STRING)
        }
    )

    @swagger_auto_schema(
        operation_description='Create a book',
        method='post',
        request_body=book_bodies,
        responses={status.HTTP_201_CREATED: BookSerializer()})
    @action(methods=['POST'], detail=False)
    def post(self, request: Request) -> Response:
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):
    """
    Retrieve, update or delete a book instance.
    """
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    book_bodies = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['title', 'desc'],
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING),
            'desc': openapi.Schema(type=openapi.TYPE_STRING)
        }
    )
    # id_param = openapi.Parameter('id',
    #                              openapi.IN_PATH,
    #                              description="The book id",
    #                              type=openapi.TYPE_INTEGER)
    update_bodies = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['title', 'desc'],
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING),
            'desc': openapi.Schema(type=openapi.TYPE_STRING)
        }
    )
    @swagger_auto_schema(
        operation_description='Update a book',
        method='put',
        request_body=book_bodies,
        responses={status.HTTP_200_OK: BookSerializer()})
    @action(methods=['PUT'], detail=False)
    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT'], detail=False)
    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
The sample code below is the same as the code \
above but uses the @api_view decorator.
search_title_config = openapi.Parameter('title',
                                        openapi.IN_QUERY,
                                        description="Search title",
                                        type=openapi.TYPE_STRING)


@swagger_auto_schema(
    method='get',
    operation_description="List all books",
    manual_parameters=[search_title_config],
    responses={
        status.HTTP_200_OK: BookSerializer(many=True)
    })
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_book_list(request: Request) -> Response:
    try:
        list_book = Book.objects.all()
        title = request.GET.get('title', None)
        if title:
            list_book = list_book.filter(title__icontains=title)

        serializer = BookSerializer(list_book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)


book_bodies = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['title', 'desc'],
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING),
        'desc': openapi.Schema(type=openapi.TYPE_STRING)
    }
)


@swagger_auto_schema(
    operation_description='Create a book',
    method='post',
    request_body=book_bodies,
    responses={status.HTTP_201_CREATED: BookSerializer()})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_book(request: Request) -> Response:
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
