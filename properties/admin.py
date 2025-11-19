from django.contrib import admin

from properties.models import Property, PropertyImage

# Register your models here.



class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 5  # Show 5 empty image forms by default
    max_num = 20  # Maximum images per property

class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ['title', 'city', 'price', 'property_type', 'purpose','is_verified',]
    list_filter = ['property_type', 'purpose', 'city', 'is_featured']
    search_fields = ['title','slug', 'description', 'city']

admin.site.register(Property, PropertyAdmin)