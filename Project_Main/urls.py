"""
URL configuration for Project_Main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django_postalcodes_mexico import urls as django_postalcodes_mexico_urls
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from rest_framework_simplejwt.views import TokenVerifyView
from seguimiento_ciudadano import urls as surls

urlpatterns = [
    path('', include("seguimiento_ciudadano.urls")),
    path('admin/', admin.site.urls),
    path('catalog/', include("catalog.urls")),
    path('cp-', include(django_postalcodes_mexico_urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include('pwa.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
