from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

class Service(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    title = models.CharField(max_length=200, help_text="Title of the service (e.g. CNC Laser Cutting)")
    slug = models.SlugField(max_length=250, unique=True, blank=True, help_text="SEO friendly URL slug. Automatically generated if left blank.")
    icon = models.CharField(max_length=100, default='fa-bolt', help_text="FontAwesome icon class name (e.g. fa-scissors, fa-microchip)")
    short_description = models.TextField(help_text="Short description shown on card list.")
    detailed_description = models.TextField(help_text="Detailed description shown on individual service page.")
    image = models.ImageField(upload_to='services/', blank=True, null=True, help_text="Feature image of the service.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    order = models.PositiveIntegerField(default=0, help_text="Display order sequence (lowest number shows first).")
    
    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200, help_text="Product name (e.g. Tower Cross Arm)")
    slug = models.SlugField(max_length=250, unique=True, blank=True, help_text="SEO friendly URL slug.")
    image = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Product display image.")
    short_description = models.TextField(help_text="Short description shown on the product card.")
    detailed_description = models.TextField(help_text="Detailed technical description.")
    specifications = models.TextField(help_text="Specification key-value list, line-separated by colon (e.g. Size: 100mm x 100mm).", blank=True)
    dimensions = models.CharField(max_length=200, blank=True, help_text="Product dimensions (e.g. 50x50x5 mm).")
    material = models.CharField(max_length=200, blank=True, help_text="Raw material (e.g. Mild Steel IS 2062).")
    applications = models.TextField(blank=True, help_text="List of applications.")
    pdf = models.FileField(upload_to='product_sheets/', blank=True, null=True, help_text="Product technical drawing or catalogue sheet.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    order = models.PositiveIntegerField(default=0, help_text="Display order sequence.")

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Gallery(models.Model):
    CATEGORY_CHOICES = (
        ('factory', 'Factory'),
        ('machines', 'Machines'),
        ('products', 'Products'),
        ('manufacturing', 'Manufacturing'),
        ('dispatch', 'Dispatch'),
        ('installation', 'Installation'),
    )
    
    title = models.CharField(max_length=200, help_text="Short title of the project image.")
    image = models.ImageField(upload_to='gallery/', help_text="Upload gallery photo.")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='factory')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery Items"

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"


class Testimonial(models.Model):
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150, help_text="e.g. Managing Director, Chief Procurement Officer")
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True, help_text="Client photograph (optional).")
    review = models.TextField(help_text="Written feedback from client.")
    rating = models.PositiveIntegerField(
        default=5, 
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating between 1 and 5 stars."
    )
    is_featured = models.BooleanField(default=True, help_text="Show in sliders on the homepage.")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.name} ({self.rating} Stars)"


class ContactRequest(models.Model):
    name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, blank=True, null=True, help_text="B2B Company Name")
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True, help_text="B2B Contact Email")
    product = models.CharField(max_length=200, blank=True, null=True, help_text="Target Product")
    quantity = models.PositiveIntegerField(default=1, help_text="Required Quantity")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False, verbose_name="Processed / Responded")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Request"
        verbose_name_plural = "Contact Requests"

    def __str__(self):
        return f"Request from {self.name} ({self.company_name or 'Individual'}) - {self.product}"
