import threading
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

from .models import Service, Product, Gallery, Testimonial, ContactRequest
from .forms import ContactRequestForm

import urllib.parse

def get_whatsapp_lead_url(contact_req, phone_number="919680711542"):
    """Generate direct WhatsApp message URL for target sales phone number."""
    text = (
        f"Hello Govindam Enterprises,\n"
        f"I am sending a Quick Inquiry for {contact_req.product}:\n\n"
        f"• Name: {contact_req.name}\n"
        f"• Company: {contact_req.company_name or 'N/A'}\n"
        f"• Mobile: {contact_req.phone}\n"
        f"• Product: {contact_req.product}\n"
        f"• Quantity: {contact_req.quantity}\n"
        f"• Details: {contact_req.message}"
    )
    encoded_text = urllib.parse.quote(text)
    return f"https://wa.me/{phone_number}?text={encoded_text}"

def send_async_email(subject, message, recipient_list):
    """Helper function to send emails asynchronously in a background thread."""
    def _send():
        try:
            from_email = getattr(settings, 'EMAIL_HOST_USER', '') or 'info@govindamenterprises.com'
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=True
            )
        except Exception as e:
            print(f"Async email notification error: {e}")

    email_thread = threading.Thread(target=_send)
    email_thread.daemon = True
    email_thread.start()

def home(request):
    products = Product.objects.filter(status='published').order_by('order')[:6]
    services = Service.objects.filter(status='published').order_by('order')[:6]
    testimonials = Testimonial.objects.filter(is_featured=True).order_by('-created_at')
    gallery_items = Gallery.objects.all().order_by('-uploaded_at')[:8]
    
    # Form processing
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            contact_req = form.save()
            whatsapp_url = get_whatsapp_lead_url(contact_req, phone_number="919680711542")
            
            # Send Notification Email to Admin
            subject = f"New B2B Lead: {contact_req.product} from {contact_req.company_name or contact_req.name}"
            email_body = (
                f"You have received a new B2B product inquiry from Govindam Enterprises Website:\n\n"
                f"Name: {contact_req.name}\n"
                f"Company Name: {contact_req.company_name or 'N/A'}\n"
                f"Mobile Number: {contact_req.phone}\n"
                f"Email: {contact_req.email or 'N/A'}\n"
                f"Requested Product: {contact_req.product}\n"
                f"Required Quantity: {contact_req.quantity}\n"
                f"Message / Details:\n{contact_req.message}\n\n"
                f"Direct WhatsApp Lead Link (+91 96807 11542): {whatsapp_url}\n"
                f"Manage this lead in Django Admin: http://{request.get_host()}/admin/website/contactrequest/{contact_req.id}/change/"
            )
            
            send_async_email(subject, email_body, [settings.EMAIL_RECEIVER])
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': "Thank you! Your quote request has been submitted successfully. Click WhatsApp below to send directly to +91 96807 11542.",
                    'whatsapp_url': whatsapp_url,
                    'target_phone': '9680711542'
                })
            
            messages.success(request, "Thank you! Your quote request has been submitted successfully. Our B2B sales team will contact you shortly.")
            return redirect('home')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                err_dict = {field: err_list[0] for field, err_list in form.errors.items()}
                return JsonResponse({'success': False, 'errors': err_dict}, status=400)
            
            messages.error(request, "Please correct the errors in the form and try again.")
    else:
        form = ContactRequestForm()

    context = {
        'products': products,
        'services': services,
        'testimonials': testimonials,
        'gallery_items': gallery_items,
        'form': form,
        'active_page': 'home'
    }
    return render(request, 'website/home.html', context)


def about(request):
    timeline = [
        {'year': '2015', 'title': 'Company Founded', 'description': 'Govindam Enterprises was established, starting with local distribution hardware trading.'},
        {'year': '2018', 'title': 'Manufacturing Setup', 'description': 'Inaugurated our first dedicated metal fabrication factory with basic punching and welding presses.'},
        {'year': '2021', 'title': 'Government Approval', 'description': 'Registered as an approved vendor for leading state electricity boards and solar contractors.'},
        {'year': '2024', 'title': 'CNC & Laser Expansion', 'description': 'Upgraded the factory floor with heavy-duty CNC Plasma and Laser cutting machinery.'},
        {'year': '2026', 'title': 'Leading B2B Supplier', 'description': 'Supplying transmission tower cross arms and steel structures across multiple state grids.'},
    ]
    
    team = [
        {'name': 'Rajesh Kumar Sharma', 'role': 'Founder & Managing Director', 'experience': '22+ Years'},
        {'name': 'Amit Kumar', 'role': 'Chief of Plant & Production', 'experience': '14+ Years'},
        {'name': 'Sunil Verma', 'role': 'Lead Quality Assurance Inspector', 'experience': '9+ Years'},
    ]
    
    context = {
        'timeline': timeline,
        'team': team,
        'active_page': 'about'
    }
    return render(request, 'website/about.html', context)


def products(request):
    query = request.GET.get('q', '').strip()
    material_filter = request.GET.get('material', '').strip()
    
    products_query = Product.objects.filter(status='published').order_by('order')
    
    if query:
        products_query = products_query.filter(
            Q(title__icontains=query) | Q(short_description__icontains=query)
        )
    if material_filter:
        products_query = products_query.filter(material__icontains=material_filter)
        
    # Get distinct materials for filters
    materials = Product.objects.filter(status='published').values_list('material', flat=True).distinct()
    materials = [m for m in materials if m]

    context = {
        'products_list': products_query,
        'materials': materials,
        'selected_material': material_filter,
        'search_query': query,
        'active_page': 'products'
    }
    return render(request, 'website/products.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, status='published')
    
    # Parse specifications line-by-line for rendering
    specs_list = []
    if product.specifications:
        for line in product.specifications.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                specs_list.append((key.strip(), val.strip()))
            elif line.strip():
                specs_list.append((line.strip(), ''))
                
    # Parse applications line-by-line
    apps_list = []
    if product.applications:
        apps_list = [line.strip() for line in product.applications.split('\n') if line.strip()]
                
    # Prepare inquiry form pre-populated with this product
    form = ContactRequestForm(initial={'product': product.title})
    
    context = {
        'product': product,
        'specs_list': specs_list,
        'apps_list': apps_list,
        'form': form,
        'active_page': 'products'
    }
    return render(request, 'website/product_detail.html', context)


def services(request):
    services_list = Service.objects.filter(status='published').order_by('order')
    context = {
        'services_list': services_list,
        'active_page': 'services'
    }
    return render(request, 'website/services.html', context)


def service_detail(request, slug):
    service_item = get_object_or_404(Service, slug=slug, status='published')
    context = {
        'service': service_item,
        'active_page': 'services'
    }
    return render(request, 'website/service_detail.html', context)


def manufacturing(request):
    # Complete B2B Manufacturing view showing processes & machinery
    processes = [
        {'step': '01', 'title': 'Raw Material Sourcing', 'desc': 'Sourcing high-quality structural steel (IS 2062 angles, channels, plates) directly from primary producers.'},
        {'step': '02', 'title': 'CNC & Plasma Cutting', 'desc': 'Precision blanking, shearing, and profiling of plates using heavy-duty CNC plasma and fiber laser machines.'},
        {'step': '03', 'title': 'Bending & Drilling', 'desc': 'Press brake bending and structural beam drilling matching customized drawing blueprints.'},
        {'step': '04', 'title': 'Welding & Assembly', 'desc': 'CO2 / MIG welding of brackets, flange joints, and structural cross arms by certified weld operators.'},
        {'step': '05', 'title': 'Hot Dip Galvanization', 'desc': 'Acid pickling followed by hot-dip zinc galvanizing (IS 2629 / BS EN ISO 1461) for robust rust resistance.'},
        {'step': '06', 'title': 'Quality & Dispatch', 'desc': 'Checking zinc coating thickness, dimensional tolerances, test reports, and dispatching in bundles.'},
    ]
    
    machines = [
        {'name': 'CNC Fiber Laser Cutting Machine', 'capacity': 'Solid plate thickness up to 20mm', 'qty': '1 Unit'},
        {'name': 'CNC Gantry Plasma Cutting Machine', 'capacity': 'Plate sizes up to 2.5m x 6m', 'qty': '1 Unit'},
        {'name': 'Heavy Structural Shearing & Punching Press', 'capacity': 'Up to 200 Tons force', 'qty': '3 Units'},
        {'name': 'MIG/CO2 Welding Stations', 'capacity': 'High-penetration structural joints', 'qty': '8 Units'},
        {'name': 'Radial Pillar Drilling Machines', 'capacity': 'Drill holes up to 50mm diameter', 'qty': '4 Units'},
    ]
    
    context = {
        'processes': processes,
        'machines': machines,
        'active_page': 'manufacturing'
    }
    return render(request, 'website/manufacturing.html', context)


def gallery(request):
    category = request.GET.get('category', '').strip()
    
    gallery_query = Gallery.objects.all()
    if category:
        gallery_query = gallery_query.filter(category=category)
        
    categories = Gallery.CATEGORY_CHOICES
    
    context = {
        'gallery_items': gallery_query,
        'categories': categories,
        'selected_category': category,
        'active_page': 'gallery'
    }
    return render(request, 'website/gallery.html', context)


def certificates(request):
    return render(request, 'website/certificates.html', {'active_page': 'certificates'})


def testimonials(request):
    testimonials_list = Testimonial.objects.all().order_by('-created_at')
    context = {
        'testimonials_list': testimonials_list,
        'active_page': 'testimonials'
    }
    return render(request, 'website/testimonials.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            contact_req = form.save()
            whatsapp_url = get_whatsapp_lead_url(contact_req, phone_number="919680711542")
            
            # Send Notification Email to Admin
            subject = f"New B2B Contact Request from {contact_req.company_name or contact_req.name}"
            email_body = (
                f"You have received a new B2B contact inquiry from Govindam Enterprises Website:\n\n"
                f"Name: {contact_req.name}\n"
                f"Company Name: {contact_req.company_name or 'N/A'}\n"
                f"Mobile Number: {contact_req.phone}\n"
                f"Email: {contact_req.email or 'N/A'}\n"
                f"Product Category: {contact_req.product}\n"
                f"Required Quantity: {contact_req.quantity}\n"
                f"Message / Details:\n{contact_req.message}\n\n"
                f"Direct WhatsApp Lead Link (+91 96807 11542): {whatsapp_url}\n"
                f"Manage this request in Django Admin: http://{request.get_host()}/admin/website/contactrequest/{contact_req.id}/change/"
            )
            
            send_async_email(subject, email_body, [settings.EMAIL_RECEIVER])
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': "Thank you! Your inquiry has been submitted successfully. Click WhatsApp below to connect with +91 96807 11542.",
                    'whatsapp_url': whatsapp_url,
                    'target_phone': '9680711542'
                })
                
            messages.success(request, "Thank you! Your inquiry has been submitted. We will get back to you shortly.")
            return redirect('contact')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                err_dict = {field: err_list[0] for field, err_list in form.errors.items()}
                return JsonResponse({'success': False, 'errors': err_dict}, status=400)
                
            messages.error(request, "Please correct the errors in the form and try again.")
    else:
        # Prepopulate with product selection if query param exists
        initial_data = {}
        preselected_product = request.GET.get('product', '').strip()
        if preselected_product:
            initial_data['product'] = preselected_product
        form = ContactRequestForm(initial=initial_data)
        
    context = {
        'form': form,
        'active_page': 'contact'
    }
    return render(request, 'website/contact.html', context)


def privacy_policy(request):
    return render(request, 'website/privacy_policy.html', {'active_page': 'privacy'})


def terms_and_conditions(request):
    return render(request, 'website/terms.html', {'active_page': 'terms'})
