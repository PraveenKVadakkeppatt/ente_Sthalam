from django.shortcuts import render

from properties import models
from properties.models import Property, PropertyImage

# Create your views here.
def home(request):
    properties = Property.objects.filter(is_verified = True,is_published=True).prefetch_related('images').select_related('listed_by')
    
    context = {
        'properties':properties,
    }
    return render(request,'home.html',context)


