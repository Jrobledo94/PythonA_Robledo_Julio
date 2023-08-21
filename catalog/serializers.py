from rest_framework import serializers
from .models import Author, Book, BookInstance, Genre, Language

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title','author','summary','isbn','genre')
    def to_representation(self, instance):
            rep = super(BookSerializer, self).to_representation(instance)
            rep['author'] = f'{instance.author.last_name}, {instance.author.first_name}'
            return rep




# Autores con una lista de sus libros en formato json
class AuthorandbooksSerializer(serializers.ModelSerializer):
    Books_list = BookSerializer(many=True, required = False)
    class Meta:
        model = Author
        fields = ('first_name','last_name','date_of_birth','date_of_death', 'Books_list')
    def create(self, validated_data):
        print(type(validated_data))
        if 'Books_list' in validated_data:
            Books_data = validated_data.pop("Books_list")
            authorr = Author.objects.create(**validated_data)
            for book in Books_data:
                bookObject = Book.objects.create(author=authorr, title=book['title'], summary=book['summary'], isbn=book['isbn'])
                for genre in book['genre']:
                    bookObject.genre.add(genre)
        else:
            authorr = Author.objects.create(**validated_data)
        return authorr



# Sólo autores, para poder agregar sólo autor
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'