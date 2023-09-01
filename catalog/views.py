from django.shortcuts import render
from django.http import Http404, HttpResponse
from .models import Book, Author, BookInstance, Genre
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AuthorSerializer, AuthorandbooksSerializer,BookInstanceSerializer,BookSerializer, SolicitudSerializer,SolicitudDetailSerializer, SeguimientoSolicitudSerializer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User


from seguimiento_ciudadano.models import Solicitudes, Seguimiento_solicitud

# Create your views here.

def index(request):
    # return render(request, 'asdasdas')
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'catalog/index.html', context=context)




class AuthorList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        all_author = Author.objects.all()
        serializers = AuthorSerializer(all_author, many=True)
        return Response(serializers.data)
    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
class AuthorBooksList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        all_author = Author.objects.all()
        serializers = AuthorandbooksSerializer(all_author, many=True)
        return Response(serializers.data)
    def post(self, request):
        serializer = AuthorandbooksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class AuthorDetail(APIView):
    def get_object(self, author_id):
        try:
            return Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            raise Http404
        
    def get(self, request, author_id):
        author = self.get_object(author_id)
        
        serializer = AuthorSerializer(author)
        return Response(serializer.data)
    def put(self, request, author_id):
        author = self.get_object(author_id)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    def delete(self, request, author_id):
        author = self.get_object(author_id)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookList(APIView):
    def get(self, request):
        all_Book = Book.objects.all()
        serializers = BookSerializer(all_Book, many=True)
        return Response(serializers.data)
    permission_classes= [IsAdminUser]
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class BookDetail(APIView):
    def get_object(self, Book_id):
        try:
            return Book.objects.get(pk=Book_id)
        except Book.DoesNotExist:
            raise Http404
        
    def get(self, request, Book_id):
        Book = self.get_object(Book_id)
        serializer = BookSerializer(Book)
        return Response(serializer.data)
    
    def put(self, request, Book_id):
        Book = self.get_object(Book_id)
        serializer = BookSerializer(Book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, Book_id):
        Book = self.get_object(Book_id)
        Book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookInstanceList(APIView):
    def get(self, request):
        all_BookInstance = BookInstance.objects.all()
        serializers = BookInstanceSerializer(all_BookInstance, many=True)
        return Response(serializers.data)
    def post(self, request):
        permission_classes = [IsAdminUser]
        serializer = BookInstanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class BookInstanceDetail(APIView):
    def get_object(self, BookInstance_id):
        try:
            return BookInstance.objects.get(pk=BookInstance_id)
        except BookInstance.DoesNotExist:
            raise Http404
        
    def get(self, request, BookInstance_id):
        BookInstance = self.get_object(BookInstance_id)
        serializer = BookInstanceSerializer(BookInstance, data=request.data)
        return Response(serializer.data)
    def put(self, request, BookInstance_id):
        BookInstance = self.get_object(BookInstance_id)
        serializer = BookInstanceSerializer(BookInstance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, BookInstance_id):
        BookInstance = self.get_object(BookInstance_id)
        BookInstance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class SolicitudesView(APIView):
    def get_permissions(self):
        print(type(self))
        print(self)
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def get(self, request):
        all_solicitudes = Solicitudes.objects.all()
        serializer = SolicitudSerializer(all_solicitudes, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = SolicitudSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    

class SolicitudesDetailView(APIView):
    def get_permissions(self):

        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        elif self.request.method == 'DELETE':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def get_object(self, Solicitud_id):
        try:
            return Solicitudes.objects.get(pk=Solicitud_id)
        except Solicitudes.DoesNotExist:
            raise Http404
    def get(self, request, Solicitud_id):
        Solicitud = self.get_object(Solicitud_id)
        serializer = SolicitudDetailSerializer(Solicitud)
        return Response(serializer.data)

    def put(self, request, Solicitud_id):
        Solicitud = self.get_object(Solicitud_id)
        serializer = SolicitudDetailSerializer(Solicitud, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, Solicitud_id):
        BookInstance = self.get_object(Solicitud_id)
        BookInstance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class SeguimientoSolicitudView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get(self, request):
        seguimientos = Seguimiento_solicitud.objects.all()
        serializer = SeguimientoSolicitudSerializer(seguimientos, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = SeguimientoSolicitudSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)