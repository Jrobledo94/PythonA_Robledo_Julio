from django.shortcuts import render
from django.http import Http404, HttpResponse
from .models import Book, Author, BookInstance, Genre
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AuthorSerializer,BookInstanceSerializer,BookSerializer,GenreSerializer,LanguageSerializer
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

class AuthorDetail(APIView):
    def get_object(self, author_id):
        try:
            return Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            raise Http404
        
    def get(self, request, author_id):
        author = self.get_object(author_id)
        serializer = AuthorSerializer(author, data=request.data)
        return Response(serializer.data)
    def put(self, request, pk):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, author_id):
        author = self.get_object(author_id)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)