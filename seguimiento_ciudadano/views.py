from django.shortcuts import render

# Create your views here.
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import F
from .models import Solicitudes
from django.views import generic, View
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import requests
import json

"""class IndexView(generic.ListView):
    template_name = "seguimiento_ciudadano/index.html"
    context_object_name = "IndexSeguimiento"""


class Index(View):
    template_name = 'seguimiento_ciudadano/solicitudes.html'
    context = {}
    context['title'] = 'Lista de Solicitudes'
    def get(self, request):
        solicitudes = Solicitudes.objects.all()
        self.context['solicitudes'] = solicitudes
        return render (request , self.template_name, self.context)


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
    if request.method == 'GET':
        return render(request, 'seguimiento_ciudadano/login.html', {"form": UserCreationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'seguimiento_ciudadano/login.html', {"form": UserCreationForm, "error": "Username or password is incorrect."})
        login(request, user)
        return redirect('seguimiento_ciudadano:index')



def solicitud(request):
    context = {}
    data = {
        "lat":41.3083,
        "long":-72.9279,
        "page_size":100,
        "page":1,
        "status":"open"
    }
    headers = {}
    r = requests.get('https://seeclickfix.com/open311/v2/requests.json',data=data)
    json_response = json.loads(r.content)

    for row in json_response:
        try:
            if not Solicitudes.objects.filter(request_id=row['service_request_id']).exists():
                soli = Solicitudes(descripcion=row['description'][:1500],
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

    context['respuesta'] = json_response
    return JsonResponse(context)