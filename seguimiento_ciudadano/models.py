from django.db import models

# Create your models here.
class Solicitudes(models.Model):
    descripcion = models.CharField(max_length=600)
    request_id = models.CharField(max_length=100)
    street_address = models.CharField(max_length=500)
    apt_number = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    zip_code = models.IntegerField()
    lat = models.IntegerField()
    long = models.IntegerField()
    solicitud_datetime =  models.DateTimeField(auto_now=True, auto_now_add=False ,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False ,null=True, blank=True)
    status = models.CharField(max_length=20)
    media_url = models.CharField(max_length=500, null = True, blank=True)
    agency_responsible = models.CharField(max_length=100, null=True, blank=True)
    activo = models.BooleanField(default=True)
    class Meta:
        ordering = ['request_id']
    def get_absolute_url(self):
        return reverse('request-detail', args=[str(self.id)])
    def __str__(self):
        return str(self.request_id)