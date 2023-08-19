from django.urls import path, include
from . import views

app_name = "seguimiento_ciudadano"
urlpatterns = [
    path("", views.Index, name="index"),
    path("solicitud", views.solicitud, name="solicitud "),
    path("login/", views.signin, name="Iniciar sesión"),
    path("logout/", views.signout, name="Logout"),
    path("registro/", views.signup, name="Registro Usuario"),
    path("ajaxEliminarSolicitud/", views.eliminarS , name="eliminar"),
    path("lista_solicitudes/", views.lista_solicitudes.as_view(), name="Lista_solicitudes"),
    path("nueva_solicitud/", views.nueva_solicitud.as_view(), name="nueva_solicitud"),
    path("<int:request_id>/seguimiento/", views.seguimiento_solicitud.as_view() , name="Seguimiento"),
    
]