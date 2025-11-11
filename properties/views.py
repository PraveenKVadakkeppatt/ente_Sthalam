from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from properties.forms import PropertyForm, PropertyImageFormSet
from properties.models import Property, PropertyImage
from django.db.models import Q
# Create your views here.

def property_details(request,slug):
    property = get_object_or_404( Property, slug = slug,is_verified = True,is_published=True)
    images = property.images.all().order_by('-is_primary', 'order')
    primary_image = images.filter(is_primary=True).first()
    features_list = property.features.split(',') if property.features else []
    if not primary_image and images:
        primary_image = images.first()
    context = {
        'property': property,
        'images': images,
        'primary_image': primary_image,
        'features_list': features_list,
    }
    return render(request,'properties/single_properties.html',context)



def properties(request):

    property_type = request.GET.get('property_type','')
    purpose = request.GET.get('purpose','')
    city = request.GET.get('city','')
    min_price = request.GET.get('min_price','')
    max_price = request.GET.get('max_price','')
    bedrooms = request.GET.get('bedrooms','')
    bathrooms = request.GET.get('bathrooms','')
    properties = Property.objects.filter(is_verified = True,is_published=True).prefetch_related('images').select_related('listed_by')

    if property_type:
        properties = properties.filter(property_type=property_type)
    if purpose:
        properties = properties.filter(purpose=purpose)
    if city:
        properties = properties.filter(city__icontains = city)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte = max_price)
    if bedrooms:
        properties = properties.filter(bedrooms__gte = int(bedrooms))
    if bathrooms:
        properties = properties.filter(bathrooms__gte = int(bathrooms))

    featured_properties = Property.objects.filter(is_featured = True,is_verified = True,is_published = True).prefetch_related('images')[:3]
    properties = properties.order_by('-is_featured', '-created_at')
    context = {
        'properties':properties,
        'featured': featured_properties,
        'property_types': Property.PROPERTY_TYPE_CHOICES,
        'purposes': Property.PURPOSE_CHOICES,
        'current_filters': {
            'property_type': property_type,
            'purpose': purpose,
            'city': city,
            'min_price': min_price,
            'max_price': max_price,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
        }
    }
    return render(request,'properties/properties.html',context)






def search_properties(request):
    purpose = request.GET.get('purpose','')
    location = request.GET.get('location','')
    property_type = request.GET.get('property_type','')
    price = request.GET.get('price','')
    bedrooms = request.GET.get('bedrooms','')
    bathrooms = request.GET.get('bathrooms','')


    properties = Property.objects.filter(is_verified=True,is_published = True).prefetch_related('images').select_related('listed_by')

    if location:
        properties = properties.filter(
            Q(city__icontains=location) | 
            Q(address__icontains=location)
        )
    
    if property_type:
        properties = properties.filter(property_type=property_type)
    
    if purpose:
        properties = properties.filter(purpose = purpose)

    if price:
        if price =='0-10000':
            properties = properties.filter(price_lte=10000)
        elif price =='10000-100000':
            properties = properties.filter(price=(10000,100000))
        elif price =='100000-500000':
            properties = properties.filter(price=(100000,500000))
        elif price =='500000-1000000':
            properties = properties.filter(price=(500000,1000000))
        elif price =='1000000-3000000':
            properties = properties.filter(price=(1000000,3000000))
        elif price =='3000000-5000000':
            properties = properties.filter(price=(3000000,5000000))
        elif price =='5000000-10000000':
            properties = properties.filter(price=(5000000,10000000))
        elif price =='10000000+':
            properties = properties.filter(price_gte=10000000)

    if bedrooms:
        if bedrooms =='5':
            properties = properties.filter(bedrooms__gte=5)
        
        else:
            properties = properties.filter(bedrooms=int(bedrooms))

    if bathrooms:
        if bathrooms =='4':
            properties = properties.filter(bathrooms__gte = 4)
        
        else:
            properties = properties.filter(bathrooms=int(bathrooms))

    properties = properties.order_by('-is_featured','-created_at')

    results_count = properties.count()

    context = {
        'properties': properties,
        'results_count': results_count,
        'search_query': {
            'location': location,
            'property_type': property_type,
            'purpose': purpose,
            'price': price,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
        },
        'property_types': Property.PROPERTY_TYPE_CHOICES,
        'purposes': Property.PURPOSE_CHOICES,
    }
    return render(request,'properties/properties.html',context)




