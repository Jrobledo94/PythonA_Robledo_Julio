from django.urls import path, include
from . import views

app_name = "seguimiento_ciudadano"
urlpatterns = [
    #path("", views.IndexView.as_view(), name="index"),
    path("", views.Index.as_view(), name="index"),
    path("solicitud", views.solicitud, name="solicitud "),
    path("login/", views.signin, name="Iniciar sesión"),
    path("logout/", views.signout, name="Logout"),
    path("registro/", views.signup, name="Registro Usuario"),
]