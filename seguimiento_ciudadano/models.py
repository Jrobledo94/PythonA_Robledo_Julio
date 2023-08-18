from django.db import models
from django.urls import reverse
import uuid

# Create your models here.

class tiposolicitud(models.Model):
    idtipoSolicitud = models.AutoField (primary_key=True)
    nombreTipoSolicitud = models.CharField('Nombre del tipo de solicitud', max_length=250, blank=True)
    def __str__(self) -> str:
            return self.nombreTipoSolicitud
    

    
class Solicitudes(models.Model):
    tipo_solicitud = models.ForeignKey(tiposolicitud, on_delete=models.RESTRICT, null=True)
    request_id = models.AutoField (primary_key=True)
    descripcion = models.CharField(max_length=1500, null=True)
    street_address = models.CharField(max_length=500)
    bld_number = models.CharField(max_length=100, null = True, blank=True)
    apt_number = models.CharField(max_length=100, null = True, blank=True)
    city = models.CharField(max_length=100, null = True, blank=True)
    state = models.CharField(max_length=100,null = True, blank=True)
    country = models.CharField(max_length=50, default='México')
    zip_code = models.IntegerField()
    colonia = models.CharField(max_length=200, null = True, blank=True)
    solicitud_datetime =  models.DateTimeField(auto_now_add=True ,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True ,null=True, blank=True)
    status = models.CharField(max_length=20, default='abierto')
    media_url = models.CharField(max_length=1000, null = True, blank=True)
    agency_responsible = models.CharField(max_length=100, null=True, blank=True)
    activo = models.BooleanField(default=True)
    class Meta:
        ordering = ['request_id']
    def get_absolute_url(self):
        return reverse('request-detail', args=[str(self.request_id)])
    def __str__(self):
        return str(self.request_id)


    




class Solicitudes_api(models.Model):
    descripcion = models.CharField(max_length=1500)
    request_id = models.CharField(max_length=100)
    street_address = models.CharField(max_length=500)
    apt_number = models.CharField(max_length=100, null = True, blank=True)
    city = models.CharField(max_length=100, null = True, blank=True)
    state = models.CharField(max_length=100,null = True, blank=True)
    country = models.CharField(max_length=50, default='US')
    zip_code = models.IntegerField()
    lat = models.FloatField()
    long = models.FloatField()
    solicitud_datetime =  models.DateTimeField(auto_now=True, auto_now_add=False ,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False ,null=True, blank=True)
    status = models.CharField(max_length=20)
    media_url = models.CharField(max_length=1000, null = True, blank=True)
    agency_responsible = models.CharField(max_length=100, null=True, blank=True)
    activo = models.BooleanField(default=True)
    class Meta:
        ordering = ['request_id']
    def get_absolute_url(self):
        return reverse('request-detail', args=[str(self.request_id)])
    def __str__(self):
        return str(self.request_id)
