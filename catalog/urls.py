from django.urls import path
from . import views

app_name = "catalog"
urlpatterns = [
    path("", views.index, name="index"),
    path('Authors_books/', views.AuthorBooksList.as_view()),
    path('Authors/', views.AuthorList.as_view(), name="Autores"),
    path('Authors/<int:author_id>/', views.AuthorDetail.as_view()),
    path('Books/', views.BookList.as_view()),
    path('Books/<int:Book_id>/', views.BookDetail.as_view()),
    path('BookInstances/', views.BookInstanceList.as_view()),
    path('BookInstances/<int:BookInstance_id>/', views.BookInstanceDetail.as_view()),
]