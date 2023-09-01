from rest_framework import serializers
from .models import Author, Book, BookInstance, Genre, Language
from seguimiento_ciudadano.models import Solicitudes, Seguimiento_solicitud
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title','author','summary','isbn','genre')
        depth = 1 # This will include the fields of the foreign key to BookInstance
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




### Seguimiento serializer class
class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitudes
        fields = '__all__'

class SeguimientoSolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguimiento_solicitud
        fields = '__all__'
        depth = 1 # This will include the fields of the foreign key to BookInstance


class SolicitudDetailSerializer(serializers.ModelSerializer):
    Seguimiento = SeguimientoSolicitudSerializer(many=True, required = False)
    class Meta:
        model=Solicitudes
        fields=('tipo_solicitud',
                'request_id',
                'descripcion',
                'street_address',
                'bld_number',
                'apt_number',
                'city',
                'state',
                'country',
                'zip_code',
                'colonia',
                'solicitud_datetime',
                'updated_at',
                'status',
                'media_url',
                'agency_responsible',
                'activo',
                'Seguimiento')
    def create(self, validated_data):
        if 'Seguimiento' in validated_data:
            Seguimiento_data = validated_data.pop("Seguimiento")
            authorr = Author.objects.create(**validated_data)
        else:
            authorr = Author.objects.create(**validated_data)
        return authorr
