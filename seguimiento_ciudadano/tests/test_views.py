from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase, Client
from django.urls import resolve, reverse
from seguimiento_ciudadano import urls
from seguimiento_ciudadano.models import Solicitudes, tiposolicitud
from seguimiento_ciudadano.views import lista_solicitudes_api, signup, seguimiento_solicitud, lista_solicitudes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.select import Select
# class urlTesting(TestCase):
#     def setUp(self) -> None:
#         self.usuario=User.objects.create_user('jrobledotest', password='Jr1811De')
#         self.usuario.is_superuser=True
#         self.usuario.is_staff=True
#         self.usuario.first_name = 'Test'
#         self.usuario.last_name = 'prueba'
#         self.usuario.save()
    
#         self.tiposoli = tiposolicitud.objects.create(nombreTipoSolicitud= "Tipo Solicitud de prueba")
#         self.solicitud = Solicitudes.objects.create(
#             tipo_solicitud=self.tiposoli,
#             descripcion = "Solicitud de prueba creado por tests ",
#             street_address = "Che Guevara",
#             bld_number = "814",
#             city= "Chihuahua",
#             state= "Chihuahua",
#             country="México",
#             zip_code=31126,
#             colonia="Tierra y Libertad",
#             status="Prueba",
#             )
#         self.url_nueva_solicitud = reverse('seguimiento_ciudadano:nueva_solicitud')
#         self.url_solicitudes = reverse('seguimiento_ciudadano:Lista_solicitudes')
#         self.url_index = reverse('seguimiento_ciudadano:index')
#         self.client = Client()




#     # def test_view_class(self):
#     #     url = reverse('seguimiento_ciudadano:Lista_solicitudes_api')
#     #     # print(resolve(url))
#     #     self.assertEqual(resolve(url).func.view_class, lista_solicitudes_api)
#     # def test_view_function(self):
#     #     url = reverse('seguimiento_ciudadano:Registro Usuario')
#     #     # print(resolve(url))
#     #     self.assertEqual(resolve(url).func.__name__, 'signup')
#     #     self.assertEqual(resolve(url).func, signup)
#     # def test_view_class_with_args(self):
#     #     url = reverse('seguimiento_ciudadano:Seguimiento', kwargs={'request_id':2})
#     #     # print(resolve(url))
#     #     self.assertEqual(resolve(url).func.view_class, seguimiento_solicitud)


#     # def test_solicitudes_get_crear_solicitud_form(self):
#     #     response = self.client.get(self.url_nueva_solicitud)
#     #     # Verificamos que el estado sea 200 (OK), es decir todo esta bien
#     #     print (response.status_code)
#     #     print('response.content:')
#     #     print(response.content)
#     #     print('response.items:')
        
#     #     print(response.items)
        
#     #     self.assertEquals(response.status_code , 401)# la vista nueva_solicitud sólo la pueden ver usuarios autenticados, arroja 401 Unauthorized
#     #     # Verificar que en la lista de Solicitudes esté el objet Solicitud creado en setUp

#     def test_solicitudes_get_all_solicitudes(self):
#         response = self.client.get(self.url_solicitudes)
#         print (response.status_code)
#         print('response.content:')
#         # print(response.content)
#         print('response.items:')
#         print(response.context['solicitudes'])
#         self.assertEquals(response.status_code , 200)# la vista nueva_solicitud sólo la pueden ver usuarios autenticados, arroja 401 Unauthorized
#         self.assertEqual(response.context['solicitudes'].first(), self.solicitud)
#         self.assertIn(self.solicitud, response.context['solicitudes'])


class test_selenium(StaticLiveServerTestCase):
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
    
        self.tiposoli = tiposolicitud.objects.create(nombreTipoSolicitud= "Tipo Solicitud de prueba")
        tiposolicitud.objects.create(nombreTipoSolicitud= "Tipo Solicitud de prueba 2")
        tiposolicitud.objects.create(nombreTipoSolicitud= "Tipo Solicitud de prueba 3")
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


    def disabled_test_1_selenium_login(self):
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
        self.browser.find_element(By.ID,'id_descripcion').send_keys('Solicitud de prueba')
        time.sleep(2)
        self.browser.find_element(By.ID,'id_street_address').send_keys('Ningún lugar')
        self.browser.find_element(By.ID,'id_bld_number').send_keys('13')
        unfocushelper = self.browser.find_element(By.ID,'id_apt_number')
        unfocushelper.send_keys('000')
        self.browser.find_element(By.ID,'id_zip_code').send_keys('31126')
        unfocushelper.click()
        unfocushelper.send_keys(Keys.SHIFT)
        unfocushelper.send_keys(Keys.TAB)
        unfocushelper.send_keys(Keys.TAB)
        time.sleep(5) #esperamos a que el javascript cargue las colonias del zip code
        colonia = Select(self.browser.find_element(By.ID,'id_colonia'))
        colonia.select_by_index(1)
        self.assertEqual(self.browser.find_element(By.ID,'id_state').text, 'Chihuahua')
        self.browser.find_element(By.XPATH,"//button[@type='submit']").click()
        time.sleep(10)
