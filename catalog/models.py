from django.db import models
from django.urls import reverse
import uuid




class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science fiction)')
    def __str__(self) -> str:
        return self.name




class Language(models.Model):
    name = models.CharField(max_length=200,help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")
    def __str__(self):
        return self.name




class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False ,null=True, blank=True)
    date_of_death = models.DateField(verbose_name='Died', auto_now=False, auto_now_add=False,null=True, blank=True)
    class Meta:
        ordering = ['last_name', 'first_name']
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])# type: ignore >como no hay un id explícito en el modelo, asuume que no existe, asi que suprimimos este 'error'
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'




class Book(models.Model):
    title = models.CharField(max_length=500)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='Books_list')
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    def __str__(self) -> str:
        return self.title
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    def display_genre(self):
    # Create a string for the Genre. This is required to display genre in Admin
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'Genre'




class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
         ('m', 'Maintenance'),
         ('o', 'On loan'),
         ('a', 'Available'),
         ('r', 'Reserved'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book Availability')
    class Meta:
        ordering = ['due_back']
    def __str__(self) -> str:
         return f'{self.id} ({self.book.title})'# type: ignore >esta vaina del Pylance no reconoce foreign keys desde dentro otro modelo
