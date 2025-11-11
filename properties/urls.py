
from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('properties',views.properties,name="properties"),
    path('property_details/<slug:slug>/',views.property_details,name='property_details'),
    path('search_properties',views.search_properties,name="search_properties"),
    path('create_property',views.create_property,name="create_property"),
    
]