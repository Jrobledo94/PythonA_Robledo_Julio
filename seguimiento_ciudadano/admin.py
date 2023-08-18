from django.contrib import admin
from seguimiento_ciudadano.models import Solicitudes, tiposolicitud
# Register your models here.
admin.site.register(Solicitudes)
admin.site.register(tiposolicitud)