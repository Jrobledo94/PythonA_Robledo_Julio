from django.urls import path
from . import views

app_name = "catalog"
urlpatterns = [
    path("", views.index, name="index"),
    path('Authors/', views.AuthorList.as_view()),
    path('Authors/<int:author_id>/', views.AuthorDetail.as_view()),
]