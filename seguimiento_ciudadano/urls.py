from django.urls import path
from . import views

app_name = "seguimiento_ciudadano"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]