from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products_by_category', args=[self.slug])

class CoffeeProduct(models.Model):
    REGION_CHOICES = [
        ('yirgacheffe', 'Yirgacheffe'),
        ('sidama', 'Sidama'),
        ('guji', 'Guji'),
        ('harrar', 'Harrar'),
        ('limu', 'Limu'),
        ('jimma', 'Jimma'),
        ('other', 'Other'),
    ]
    
    PROCESS_CHOICES = [
        ('washed', 'Washed'),
        ('natural', 'Natural'),
        ('honey', 'Honey'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    region = models.CharField(max_length=50, choices=REGION_CHOICES)
    process = models.CharField(max_length=20, choices=PROCESS_CHOICES)
    roast_level = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text="Weight in grams")
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Images
    main_image = models.ImageField(upload_to='products/')
    image_2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relationships
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.region})"
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])
    
    @property
    def price_per_kg(self):
        return (self.price / self.weight) * 1000 if self.weight > 0 else 0
    
    @property
    def is_in_stock(self):
        return self.stock > 0 and self.is_available