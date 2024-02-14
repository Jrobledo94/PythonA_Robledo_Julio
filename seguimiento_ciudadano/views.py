from django.shortcuts import render

# Create your views here.
from .forms import CustomUserCreationForm, SolicitudForm, ActividadSeguimientoForm, SolicitudStatusForm
from .models import Solicitudes_api, Solicitudes, Seguimiento_solicitud
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import requests

"""class IndexView(generic.ListView):
    template_name = "seguimiento_ciudadano/index.html"
    context_object_name = "IndexSeguimiento"""


def Index(request):
    if request.user.is_active:
        template_name = 'seguimiento_ciudadano/index.html'
        context = {}
        context['title'] = 'Lista de Solicitudes'
        return render (request , template_name, context)
    else:
        return redirect("login/")


def signin(request):
    if not request.user.is_active:
        if request.method == 'GET':
            return render(request, 'seguimiento_ciudadano/login.html', {"form": AuthenticationForm})
        else:
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, 'seguimiento_ciudadano/login.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})
            login(request, user)
            return redirect('seguimiento_ciudadano:index')
    else:
        return redirect('seguimiento_ciudadano:index')
    

def signout(request):
    logout(request)
    return redirect('seguimiento_ciudadano:index')


def signup(request):
    context = {}
    if request.method == 'GET':
        context['form'] = CustomUserCreationForm
        return render(request, 'seguimiento_ciudadano/register.html', context)
    else:
        form = CustomUserCreationForm(request.POST)  
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='ciudadano')
            user.groups.add(group)
            login(request, user)
            #messages.success(request, 'Registro Exitoso!')
        else:
            return render(request, 'seguimiento_ciudadano/register.html', {'form':form})
        return redirect('seguimiento_ciudadano:index')
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def eliminarS(request):
    context = {}
    if request.method == 'POST':
        id = int(request.POST.get('id'))
        Solicitudes.objects.filter(pk=id).delete()
        return HttpResponse("Solicitud_Eliminada_True")
    else:
        return HttpResponse("Error: Method can only be POST")
        


class lista_solicitudes(View):
    template_name = 'seguimiento_ciudadano/solicitudes.html'
    context = {}
    context['title'] = 'Lista de Solicitudes'
    def get(self, request):
        solicitudes = Solicitudes.objects.all()
        self.context['solicitudes'] = solicitudes
        return render(request , self.template_name, self.context)
class lista_solicitudes_api(View):
    template_name = 'seguimiento_ciudadano/solicitudes_api.html'
    context = {}
    context['title'] = 'Lista de Solicitudes'
    def get(self, request):
        solicitudes = Solicitudes_api.objects.all()
        self.context['solicitudes'] = solicitudes
        return render(request , self.template_name, self.context)

    

class nueva_solicitud(APIView):
    permission_classes = [IsAuthenticated]
    template_name ='seguimiento_ciudadano/agregar_solicitud.html'
    context = {}
    context['title'] = 'Generar nueva solicitud'
    #def post(self, request):
    def get(self, request):
        self.context['form'] = SolicitudForm()
        return render(request, self.template_name, self.context)
    def post(self, request):
        formulario=SolicitudForm(data=request.POST or None )
        if formulario.is_valid():
            print("Valido")
            soli_a_guardar = formulario.save()
            try:
                upload = request.FILES['media_url']
                fss = FileSystemStorage()
                file = fss.save(upload.name, upload)
                file_url = fss.url(file)
                soli_a_guardar.media_url = file_url
                soli_a_guardar.save()
            except Exception as e:
                print(str(e))
            messages.success(request, 'Se guardo correctamente')
        else:
            print(formulario.errors.as_data())
        return render(request , 'seguimiento_ciudadano/index.html', self.context)



class seguimiento_solicitud(View):
    template_name="seguimiento_ciudadano/seguimiento_solicitud.html"
    context = {}
    
    def get(self, request, request_id):
        soli = get_object_or_404(Solicitudes, pk=request_id)
        actividades = Seguimiento_solicitud.objects.filter(solicitud_id = soli)
        self.context["Solicitud"]  = soli
        self.context['formSolicitud'] = SolicitudStatusForm(instance=soli)
        self.context["formActividad"] = ActividadSeguimientoForm()
        self.context['seguimiento_solicitud'] = actividades
        return render(request, self.template_name, self.context)
    def post(self, request, request_id):
        formularioActividad=ActividadSeguimientoForm(data=request.POST or None )
        formularioSolicitud=SolicitudStatusForm(data=request.POST or None )
        Solicitud = Solicitudes.objects.get(pk=request_id)
        Solicitud.status = request.POST['status']
        Solicitud.save()
        if formularioActividad.is_valid() and formularioSolicitud.is_valid():
            print("Valido")
            try:
                actividad = formularioActividad.save(commit=False)
                actividad.solicitud_id = Solicitud
                upload = request.FILES['evidencia']
                fss = FileSystemStorage()
                file = fss.save(upload.name, upload)
                file_url = fss.url(file)
                actividad.evidencia = file_url
                actividad.save()
            except Exception as e:
                print(str(e))
            messages.success(request, 'Se guardo correctamente')
            self.context['request_id'] = request_id
            return redirect(request.META['HTTP_REFERER'])
        return render (request , 'seguimiento_ciudadano/index.html', self.context)

def solicitud(request):
    json_pages = []
    context={}
    for page in range(1,5):
        context = {}
        data = {
            "lat":41.3083,
            "long":-72.9279,
            "page_size":200,
            "page":page,
            "status":"open"
        }
        headers = {}
        r = requests.get('https://seeclickfix.com/open311/v2/requests.json',data=data)
        json_response = json.loads(r.content)
        if page == 1:
            json_pages = json.loads(r.content)
        for row in json_response:
            try:
                if not Solicitudes_api.objects.filter(request_id=row['service_request_id']).exists():
                    soli = Solicitudes_api(descripcion=row['description'][:1500],
                                    request_id=row['service_request_id'],
                                    solicitud_datetime=row['requested_datetime'],
                                    street_address=row['address'],
                                    zip_code = row['zipcode'], 
                                    lat = row['lat'],
                                    long = row['long'],
                                    media_url = row['media_url'],
                                    agency_responsible = row['agency_responsible'],
                                    status = row['status']
                                    )
                
                    soli.save()
            except Exception as e:
                print(str(e))
        if page >1: json_pages.append(json_response)
    context['respuesta'] = json_pages
    return JsonResponse(context)