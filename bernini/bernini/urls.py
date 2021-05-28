"""bernini URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework import routers
from bernini.views import UserViewSet
from products.urls import router as products_router
from carts.urls import router as carts_router

# API Root - Router
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.registry.extend(products_router.registry)
router.registry.extend(carts_router.registry)

schema_url_patterns = [
    path('', include('bernini.urls')),
]

schema = get_schema_view(
    title="Bernini API", 
    description="API for ecommerce",
    url="http://localhost:8000",
    patterns=schema_url_patterns,
    version="1.0.0")

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls), # panel admin
    path('api-auth/', include('rest_framework.urls')), # login default de rest framework
    path('doc/', schema, name='openapi-schema'),
]
