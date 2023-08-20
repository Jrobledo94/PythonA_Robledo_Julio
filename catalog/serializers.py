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

class AuthorSerializer(serializers.ModelSerializer):
    print('entre al authorserializer')
    Books_list = BookSerializer(many=True)
    class Meta:
        model = Author
        fields = ('first_name','last_name','date_of_birth','date_of_death', 'Books_list')
    def create(self, validated_data):
        Books_data = validated_data.pop("Books_list")
        authorr = Author.objects.create(**validated_data)
        for book in Books_data:
            bookObject = Book.objects.create(author=authorr, title=book['title'], summary=book['summary'], isbn=book['isbn'])
            for genre in book['genre']:
                bookObject.genre.add(genre)
        return authorr

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