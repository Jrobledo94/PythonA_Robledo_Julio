from django.contrib import admin
from seguimiento_ciudadano.models import Solicitudes, tiposolicitud, Seguimiento_solicitud
# Register your models here.
admin.site.register(tiposolicitud)
admin.site.register(Seguimiento_solicitud)
@admin.register(Solicitudes)
class SolicitudesAdmin(admin.ModelAdmin):
    readonly_fields = ('solicitud_datetime','updated_at')

