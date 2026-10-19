import csv
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from .models import Service, Product, Gallery, Testimonial, ContactRequest

class GovindamAdminSite(AdminSite):
    site_header = "Govindam Enterprises Administration"
    site_title = "Govindam Admin Portal"
    index_title = "Welcome to Govindam Enterprises Management Dashboard"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Dynamic stats context for admin index template
        extra_context['total_products'] = Product.objects.count()
        extra_context['total_services'] = Service.objects.count()
        extra_context['total_gallery'] = Gallery.objects.count()
        extra_context['total_testimonials'] = Testimonial.objects.count()
        extra_context['pending_requests'] = ContactRequest.objects.filter(is_processed=False).count()
        extra_context['total_requests'] = ContactRequest.objects.count()
        return super().index(request, extra_context=extra_context)

# Instantiate the custom admin site
admin_site = GovindamAdminSite(name='govindam_admin')

# Register default Auth models
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

# Product admin customization
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'material', 'dimensions', 'order', 'status', 'slug')
    list_editable = ('order', 'status')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description', 'material')
    list_filter = ('status', 'material')
    fieldsets = (
        ('Product Details', {
            'fields': ('title', 'slug', 'image', 'short_description', 'detailed_description')
        }),
        ('Technical Specs', {
            'fields': ('specifications', 'dimensions', 'material', 'applications', 'pdf')
        }),
        ('Display Settings', {
            'fields': ('status', 'order')
        }),
    )

# Service admin customization
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'order', 'slug')
    list_editable = ('status', 'order')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description')
    list_filter = ('status',)
    fieldsets = (
        ('Service Details', {
            'fields': ('title', 'slug', 'icon', 'short_description', 'detailed_description')
        }),
        ('Media & Display Settings', {
            'fields': ('image', 'status', 'order')
        }),
    )

# Gallery admin customization
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_at')
    list_filter = ('category', 'uploaded_at')
    search_fields = ('title',)

# Testimonial admin customization
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'rating', 'is_featured')
    list_filter = ('rating', 'is_featured')
    search_fields = ('name', 'review')

# ContactRequest admin customization
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'phone', 'email', 'product', 'quantity', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'company_name', 'phone', 'message', 'product')
    readonly_fields = ('name', 'company_name', 'phone', 'email', 'product', 'quantity', 'message', 'created_at')
    actions = ['mark_as_processed', 'export_to_csv']

    def mark_as_processed(self, request, queryset):
        rows_updated = queryset.update(is_processed=True)
        self.message_user(request, f"{rows_updated} requests successfully marked as processed.")
    mark_as_processed.short_description = "Mark selected requests as Processed"

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="contact_requests.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Company Name', 'Phone', 'Email', 'Product', 'Quantity', 'Message', 'Created At', 'Processed'])
        for r in queryset:
            writer.writerow([r.name, r.company_name, r.phone, r.email, r.product, r.quantity, r.message, r.created_at, r.is_processed])
        return response
    export_to_csv.short_description = "Export selected requests to CSV"

# Register custom models to the custom admin site
admin_site.register(Product, ProductAdmin)
admin_site.register(Service, ServiceAdmin)
admin_site.register(Gallery, GalleryAdmin)
admin_site.register(Testimonial, TestimonialAdmin)
admin_site.register(ContactRequest, ContactRequestAdmin)
