from django.test import SimpleTestCase, TestCase, Client
from django.urls import resolve, reverse
from seguimiento_ciudadano.views import lista_solicitudes_api, signup, seguimiento_solicitud, lista_solicitudes
from seguimiento_ciudadano import urls
from seguimiento_ciudadano.models import Solicitudes, tiposolicitud

class urlTesting(TestCase):
    def setUp(self) -> None:

        self.tiposoli = tiposolicitud.objects.create(nombreTipoSolicitud= "Tipo Solicitud de prueba")
        self.solicitud = Solicitudes.objects.create(
            tipo_solicitud=self.tiposoli,
            descripcion = "Solicitud de prueba creado por tests ",
            street_address = "Che Guevara",
            bld_number = "814",
            city= "Chihuahua",
            state= "Chihuahua",
            country="México",
            zip_code=31126,
            colonia="Tierra y Libertad",
            status="Prueba",
            )
        self.url_solicitudes = reverse('seguimiento_ciudadano:Lista_solicitudes')
        self.client = Client()




    def test_view_class(self):
        url = reverse('seguimiento_ciudadano:Lista_solicitudes_api')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, lista_solicitudes_api)
    def test_view_function(self):
        url = reverse('seguimiento_ciudadano:Registro Usuario')
        print(resolve(url))
        self.assertEqual(resolve(url).func.__name__, 'signup')
        self.assertEqual(resolve(url).func, signup)
    def test_view_class_with_args(self):
        url = reverse('seguimiento_ciudadano:Seguimiento', kwargs={'request_id':2})
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, seguimiento_solicitud)


    def test_solicitudes_get_all_solicitudes(self):
        response = self.client.get(self.url_solicitudes)
        # Verificamos que el estado sea 200 (OK), es decir todo esta bien
        self.assertEquals(response.status_code , 200)# OK
        