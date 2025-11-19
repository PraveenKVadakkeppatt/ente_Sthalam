from django import forms
from .models import Property, PropertyImage
from django.forms import BaseModelFormSet

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        exclude = ['slug', 'listed_by', 'is_verified', 'is_featured', 'is_published', 'created_at', 'updated_at']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter property description...',
                'style': 'resize: vertical; width: 100%; min-height: 100px;'
            }),
            'address': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Enter property Address...',
                'style': 'resize: vertical; width: 100%; min-height: 60px;'
            }),
            'features': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Comma separated features (e.g. Pool, Gym, Parking)',
                'style': 'resize: vertical; width: 100%; min-height: 100px;'
            }),
        }

    image1 = forms.ImageField(required=True)
    image1_caption = forms.CharField(required=False)
    image1_primary = forms.BooleanField(required=False)

    image2 = forms.ImageField(required=False)
    image2_caption = forms.CharField(required=False)
    image2_primary = forms.BooleanField(required=False)

    image3 = forms.ImageField(required=False)
    image3_caption = forms.CharField(required=False)
    image3_primary = forms.BooleanField(required=False)

    image4 = forms.ImageField(required=False)
    image4_caption = forms.CharField(required=False)
    image4_primary = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['placeholder'] = "Enter the Title of Property"
        self.fields['property_type'].widget.attrs['placeholder'] = "Select the Property type"
        self.fields['purpose'].widget.attrs['placeholder'] = "Select the Purpose type"
        self.fields['price'].widget.attrs['placeholder'] = "Enter the Price"
        self.fields['address'].widget.attrs['placeholder'] = "Enter the Address"
        self.fields['city'].widget.attrs['placeholder'] = "Enter the City"
        self.fields['location_latitude'].widget.attrs['placeholder'] = 'Add the Location Latitude'
        self.fields['location_longitude'].widget.attrs['placeholder'] = 'Add the Location Longitude'
        self.fields['bedrooms'].widget.attrs['placeholder'] = 'Add the Number of Bedrooms'
        self.fields['bathrooms'].widget.attrs['placeholder'] = 'Add the Number of Bathrooms'
        self.fields['parking_spaces'].widget.attrs['placeholder'] = 'Add the Number of Parking Spaces'
        self.fields['area_sqft'].widget.attrs['placeholder'] = 'Enter Total Area Sqft'
        self.fields['furnishing'].widget.attrs['placeholder'] = 'Select the Option'
        self.fields['building_name'].widget.attrs['placeholder'] = 'Enter the Building Name'
        self.fields['floor_number'].widget.attrs['placeholder'] = 'Enter the Floor Number'
        self.fields['total_floors'].widget.attrs['placeholder'] = 'Enter the Number of Floors'
        self.fields['year_built'].widget.attrs['placeholder'] = 'Enter the Year Built'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        for i in range(1, 5):
            self.fields[f'image{i}_primary'].widget.attrs['class'] = 'form-check-input'

    
    def clean(self):
        cleaned_data = super().clean()

        primary_count = 0
        for i in range(1, 5):
            if cleaned_data.get(f'image{i}_primary'):
                primary_count += 1

        if primary_count > 1:
            raise forms.ValidationError("Only one primary image can be selected.")

        return cleaned_data


# class PropertyImageForm(forms.ModelForm):
#     class Meta:
#         model = PropertyImage
#         fields = ['image', 'caption', 'is_primary', 'order']
#         widgets = {
#             'caption': forms.TextInput(attrs={'class': 'form-control'}),
#             'order': forms.NumberInput(attrs={'class': 'form-control'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['image'].widget.attrs.update({'class': 'form-control image-input'})
#         self.fields['is_primary'].widget.attrs.update({'class': 'form-check-input primary-checkbox'})



# class PropertyImageBaseFormSet(BaseModelFormSet):

#     def clean(self):
#         super().clean()

#         image_count = 0
#         primary_count = 0

#         for form in self.forms:
#             if form.cleaned_data.get('image'):
#                 image_count += 1

#             if form.cleaned_data.get('is_primary'):
#                 primary_count += 1

#         if image_count < 6:
#             raise forms.ValidationError("At least 6 property images are required.")

#         if primary_count == 0:
#             raise forms.ValidationError("Please mark one image as the primary image.")
        
#         if primary_count > 1:
#             raise forms.ValidationError("Only one image can be selected as primary.")