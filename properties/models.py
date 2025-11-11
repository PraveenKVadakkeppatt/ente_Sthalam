from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils.text import slugify
from users.models import Account
# Create your models here.



class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('townhouse', 'Townhouse'),
        ('penthouse', 'Penthouse'),
        ('residential_plot', 'Residential Plot'),
        ('commercial', 'Commercial'),
        ('office', 'Office'),
        ('warehouse', 'Warehouse'),
        ('land', 'Land'),
    ]

    PURPOSE_CHOICES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    ]
    FURNISHING_CHOICES = [
        ('furnished', 'Fully Furnished'),
        ('unfurnished', 'Unfurnished'),
        ('partially', 'Partially Furnished'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250,unique=True,blank=True)
    description = models.TextField()
    property_type = models.CharField(max_length=50,choices=PROPERTY_TYPE_CHOICES)
    purpose = models.CharField(max_length=10,choices=PURPOSE_CHOICES,default='sale')
    price = models.DecimalField(max_digits=12,decimal_places=2)
    address = models.TextField()
    city = models.CharField(max_length=100)
    # For maps integration
    location_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    location_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    parking_spaces = models.PositiveIntegerField(default=0)
    area_sqft = models.DecimalField(max_digits=8, decimal_places=2)
    furnishing = models.CharField(max_length=100,choices=FURNISHING_CHOICES,default='unfurnished')
    features = models.TextField(blank=True)  # Comma-separated features
    # === Building Information ===
    building_name = models.CharField(max_length=100, blank=True)
    floor_number = models.IntegerField(blank=True, null=True)
    total_floors = models.IntegerField(blank=True, null=True)
    year_built = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2030)],
        blank=True, null=True
    )

    listed_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='properties')
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.generate_slug()
        
        super().save(*args, **kwargs)
    
    def generate_slug(self):
        base_slug = slugify(f"{self.title} {self.city}")
        
        if len(base_slug) > 240:
            base_slug = base_slug[:240]
        
        slug = base_slug
        counter = 1
        
        # Ensure slug is unique
        while Property.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
            # Safety break to prevent infinite loops
            if counter > 1000:
                import uuid
                slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
                break
        
        self.slug = slug
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/property/{self.slug}/"

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['purpose', 'property_type']),
            models.Index(fields=['city', 'price']),
            models.Index(fields=['is_featured', 'is_published']),
        ]

    


class PropertyImage(models.Model):
    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='properties_images/')
    caption = models.CharField(max_length=200,blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)