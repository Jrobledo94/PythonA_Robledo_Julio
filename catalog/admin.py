from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language

# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(Genre)
# admin.site.register(BookInstance)
# admin.site.register(Language)


class BookInline(admin.TabularInline):
    model = Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # Afecta a la vista en el admin, aquí seleccionas qué campos verás en la lista general 
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # fields afecta a la vista al agregar, por default todos los campos aparecen vertical, pero se puede cambiar esto con las tuplas, representadas con () #
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]



# BookInstanceInline es una clase que añade a la vista del libro, una sección para que directo del libro, puedas agregar bookinstances al agregar un libro (o al editarlo)
class BookInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'imprint', 'status', 'due_back')
    # List_filter agrega una columna en la vista de lista BookInstance, para filtrar la lsita por los campos seleccionados
    list_filter = ('status', 'due_back')

    # Con este fieldsets, divides la vista al ver los detalles de un bookinstance, creando un banner para dividir la sección de la disponibilidad del libro
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass