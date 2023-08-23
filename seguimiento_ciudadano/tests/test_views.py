import json
from catalog import models as catModels
from django_postalcodes_mexico.models import PostalCode
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import SimpleTestCase, TestCase, Client
from django.urls import resolve, reverse
from seguimiento_ciudadano import urls
from seguimiento_ciudadano.models import Solicitudes, tiposolicitud
from seguimiento_ciudadano.views import lista_solicitudes_api, signup, seguimiento_solicitud, lista_solicitudes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import time
from django.conf import settings


"""
class unitTesting(TestCase):
    def setUp(self) -> None:
        self.usuario=User.objects.create_user('jrobledotest', password='Jr1811De')
        self.usuario.is_superuser=True
        self.usuario.is_staff=True
        self.usuario.first_name = 'Test'
        self.usuario.last_name = 'prueba'
        self.usuario.save()
  
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
        self.url_nueva_solicitud = reverse('seguimiento_ciudadano:nueva_solicitud')
        self.url_solicitudes = reverse('seguimiento_ciudadano:Lista_solicitudes')
        self.url_index = reverse('seguimiento_ciudadano:index')
        self.client = Client()
    def test_view_class(self):
        url = reverse('seguimiento_ciudadano:Lista_solicitudes_api')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, lista_solicitudes_api)
    def test_view_function(self):
        url = reverse('seguimiento_ciudadano:Registro Usuario')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.__name__, 'signup')
        self.assertEqual(resolve(url).func, signup)
    def test_view_class_with_args(self):
        url = reverse('seguimiento_ciudadano:Seguimiento', kwargs={'request_id':2})
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, seguimiento_solicitud)
    def test_solicitudes_get_crear_solicitud_form(self):
        response = self.client.get(self.url_nueva_solicitud)
        # Verificamos que el estado sea 200 (OK), es decir todo esta bien
        print (response.status_code)
        print('response.content:')
        print(response.content)
        print('response.items:')
        print(response.items)
        self.assertEquals(response.status_code , 401)# la vista nueva_solicitud sólo la pueden ver usuarios autenticados, arroja 401 Unauthorized
        # Verificar que en la lista de Solicitudes esté el objet Solicitud creado en setUp
    def test_solicitudes_get_all_solicitudes(self):
        response = self.client.get(self.url_solicitudes)
        print (response.status_code)
        print('response.content:')
        # print(response.content)
        print('response.items:')
        print(response.context['solicitudes'])
        self.assertEquals(response.status_code , 200)# la vista nueva_solicitud sólo la pueden ver usuarios autenticados, arroja 401 Unauthorized
        self.assertEqual(response.context['solicitudes'].first(), self.solicitud)
        self.assertIn(self.solicitud, response.context['solicitudes'])





class test_funcional_selenium(StaticLiveServerTestCase):
    def setUp(self):
        self.options = Options()
        self.options.page_load_strategy = 'normal'   
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(2)
        self.browser.maximize_window
        self.wait = WebDriverWait(self.browser, timeout=3)
        self.usuario=User.objects.create_user('jrobledotest', password='Jr1811De')
        self.usuario.is_superuser=True
        self.usuario.is_staff=True
        self.usuario.first_name = 'Test'
        self.usuario.last_name = 'prueba'
        self.usuario.save()
        self.zipcode = PostalCode.objects.create(d_codigo='01140', d_asenta='José Maria Pino Suárez',D_mnpio='Álvaro Obregón', d_ciudad='Ciudad de México', c_estado= '09',c_oficina= '01131',c_tipo_asenta= '09',c_mnpio= '010',id_asenta_cpcons= '0060',d_zona= 'Urbano',c_cve_ciudad= '01',d_CP= '01131')
        self.zipcode.save()

        self.tiposoli = tiposolicitud.objects.create(nombreTipoSolicitud= "Tipo Solicitud de prueba")
        tiposolicitud.objects.create(nombreTipoSolicitud= "Tipo Solicitud de prueba 2")
        tiposolicitud.objects.create(nombreTipoSolicitud= "Tipo Solicitud de prueba 3")
        self.solicitud = Solicitudes.objects.create(tipo_solicitud=self.tiposoli,descripcion = "Solicitud de prueba creado por tests ",street_address = "Che Guevara",bld_number = "814",city= "Chihuahua",state= "Chihuahua",country="México",zip_code=31126,colonia="Tierra y Libertad",status="Prueba")
        self.url_nueva_solicitud = reverse('seguimiento_ciudadano:nueva_solicitud')
        self.url_solicitudes = reverse('seguimiento_ciudadano:Lista_solicitudes')
        self.url_index = reverse('seguimiento_ciudadano:index')
        self.descripcion = "Solicitud de prueba"



    def test_1_selenium_login(self):
        self.browser.maximize_window()
        print(self.live_server_url)
        self.browser.get(self.live_server_url)
        time.sleep(1)
        print(self.browser.find_element(By.XPATH, "//a[contains(@href,'login')]//parent::button"))
        self.browser.find_element(By.XPATH, "//a[contains(@href,'login')]//parent::button").click()
        self.browser.find_element(By.ID, "username").send_keys('jrobledotest')
        
        self.browser.find_element(By.NAME, "password").send_keys('Jr1811De')
        time.sleep(1)
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()
        self.wait.until(lambda d : self.browser.find_element(By.XPATH,"//div[@class='header-nav']//child::a[last()]//div").is_displayed)
        print(self.browser.find_element(By.XPATH,"//div[@class='header-nav']//child::a[last()]//div").text)
        self.assertEqual(self.browser.find_element(By.XPATH,"//div[@class='header-nav']//child::a[last()]//div").text, 'Cerrar Sesión')
        print(self.browser.find_element(By.ID,"btn-usuario").text)
        self.assertIn(self.browser.find_element(By.ID,"btn-usuario").text, 'Test Prueba')

    def test_2_selenium_crear_solicitud(self):


        self.browser.maximize_window()
        print(self.live_server_url)
        self.browser.get(self.live_server_url)
        time.sleep(1)
        print(self.browser.find_element(By.XPATH, "//a[contains(@href,'login')]//parent::button"))
        self.browser.find_element(By.XPATH, "//a[contains(@href,'login')]//parent::button").click()
        self.browser.find_element(By.ID, "username").send_keys('jrobledotest')
        
        self.browser.find_element(By.NAME, "password").send_keys('Jr1811De')
        time.sleep(1)
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()
        self.wait.until(lambda d : self.browser.find_element(By.XPATH,"//div[@class='header-nav']//child::a[last()]//div").is_displayed)
        print(self.browser.find_element(By.XPATH,"//div[@class='header-nav']//child::a[last()]//div").text)
        self.assertEqual(self.browser.find_element(By.XPATH,"//div[@class='header-nav']//child::a[last()]//div").text, 'Cerrar Sesión')
        print(self.browser.find_element(By.ID,"btn-usuario").text)
        self.assertIn(self.browser.find_element(By.ID,"btn-usuario").text, 'Test Prueba')
        # Seleccionamos la opción para crear una nueva solicitud
        self.browser.find_element(By.XPATH, "//div[@class='header-content']//descendant::div[text()='Crear Solicitud']//parent::a").click()
        tipo = Select(self.browser.find_element(By.ID,'id_tipo_solicitud'))
        time.sleep(2)
        tipo.select_by_index(2)
        self.browser.find_element(By.ID,'id_descripcion').send_keys(self.descripcion)
        time.sleep(2)
        self.browser.find_element(By.ID,'id_street_address').send_keys('Ningún lugar')
        self.browser.find_element(By.ID,'id_bld_number').send_keys('13')
        unfocushelper = self.browser.find_element(By.ID,'id_apt_number')
        unfocushelper.send_keys('000')
        self.browser.find_element(By.ID,'id_zip_code').send_keys('01140')
        unfocushelper.click()
        unfocushelper.send_keys(Keys.SHIFT)
        self.browser.find_element(By.ID,'id_descripcion').send_keys(Keys.TAB)
        self.browser.find_element(By.ID,'id_descripcion').send_keys(Keys.TAB)
        time.sleep(5) #esperamos a que el javascript cargue las colonias del zip code
        colonia = Select(self.browser.find_element(By.ID,'id_colonia'))
        for option in colonia.options:
            print(option)
            print(option.id)
            print(option.text)
        time.sleep(5) #esperamos a que el javascript cargue las colonias del zip code
        colonia.select_by_value(self.zipcode.d_asenta)
        print(self.browser.find_element(By.ID,'id_state').text)
        self.assertEqual(self.browser.find_element(By.NAME,'state').get_attribute('value'), self.zipcode.D_mnpio)
        self.browser.find_element(By.XPATH,"//button[@type='submit']").click()
        time.sleep(2)
        print(self.browser.find_element(By.CLASS_NAME,"toast-body"))
        self.assertTrue(self.browser.find_element(By.CLASS_NAME,"toast-body").is_displayed)
        self.assertEquals(self.browser.find_element(By.CLASS_NAME,"toast-body").text,"Se guardo correctamente")

        self.browser.find_element(By.XPATH,"//div[text()='Ver Solicitudes']//parent::a").click()
        time.sleep(2)# esperamos 2 segundos por si hay alguna otra petición en proceso
        self.assertIn(self.browser.find_element(By.XPATH, "//table"), self.descripcion)
        #end test
         """


class TestIntegraciónAPI(TestCase):
    def setUp(self) -> None:
        self.usuario=User.objects.create_user('jrobledotest', password="Jr1811De")
        self.usuario.is_superuser=True
        self.usuario.is_staff=True
        self.usuario.first_name = 'Test'
        self.usuario.last_name = 'prueba'
        self.usuario.save()
        self.Autor = catModels.Author.objects.create(first_name="Howard Phillips", last_name="Lovecraft" , date_of_birth="1890-08-20", date_of_death="1937-03-15")
        self.Autor = catModels.Author.objects.create(first_name="Stephen", last_name="King" , date_of_birth="1947-09-21")
        self.client = Client()
        self.url_Authors = reverse('catalog:Autores')
        self.url_api_token = reverse('token_obtain_pair')
        self.access=""
        self.refresh=""
        return super().setUp()
    


    def test_get_authors_and_authorization(self):
        response = self.client.get(self.url_Authors)
        print(response.content)
        print(response.status_code)
        self.assertEquals(response.status_code , 401) #No autorizado, necesita recibir el token e iniciar sesión



        ### Obtener Token
        authjson = {
            "username":self.usuario.username,
            "password":"Jr1811De",
        }

        authRequest = self.client.post(self.url_api_token, authjson, format="json")
        time.sleep(2)
        print(authRequest)
        print(authRequest.status_code)
        print(authRequest.content)
        self.assertEqual(authRequest.status_code,200)
        accessJson = json.loads(authRequest.content)
        self.access = str("Bearer "+str(accessJson["access"]))
        self.refresh = str(accessJson["refresh"])
        print(self.access)
        self.assertIn(accessJson["access"],self.access )
        ###


        ### lista de autores
        print("Getting author list...")
        time.sleep(1)
        clientWithToken = Client(HTTP_AUTHORIZATION=self.access) #necesaria una instancia nueva para agregar al header el token de acceso, las otras formas que encontré (client.credentials, **header o **extra) no jalaron
        response = clientWithToken.get(self.url_Authors)
        print(response.content)
        print(response.status_code)
        self.assertEquals(response.status_code , 200)
        ###

        ###agregar un autor
        jsonAuthor = {
            "first_name": "Juana de",
            "last_name": "Arco",
            "date_of_birth": "1968-08-17",
            "date_of_death": "2014-12-24"
        }
        POSTauthorRequest = clientWithToken.post(self.url_Authors, data=jsonAuthor)
        print(POSTauthorRequest.content)
        print(POSTauthorRequest.status_code)
        self.assertEquals(POSTauthorRequest.status_code , 201)
        self.assertEqual(jsonAuthor["last_name"],json.loads(POSTauthorRequest.content)["last_name"])


        ### Prueba de objeto con response
        created_author = catModels.Author.objects.get(first_name="Juana de")
        self.assertEqual(created_author.last_name, jsonAuthor["last_name"])

