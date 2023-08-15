from django.shortcuts import render

# Create your views here.
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
# from .models import Question, Choice
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout



class IndexView(generic.ListView):
    template_name = "seguimiento_ciudadano/index.html"
    context_object_name = "IndexSeguimiento"


def signin(request):
    if request.method == 'GET':
        return render(request, 'seguimiento_ciudadano/login.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'seguimiento_ciudadano/login.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})
        login(request, user)
        return redirect('seguimiento_ciudadano:vote')