from django.test import TestCase, Client
from django.urls import reverse
from .models import Service, Product, Gallery, Testimonial, ContactRequest
from .forms import ContactRequestForm

class GovindamWebsiteTests(TestCase):
    
    def setUp(self):
        # Create sample product
        self.product = Product.objects.create(
            title="Tower Cross Arm",
            short_description="High-strength cross arms.",
            detailed_description="Detailed specs for Tower Cross Arms.",
            specifications="Size: 100mm",
            dimensions="100x100x8 mm",
            material="Structural Steel",
            applications="Substations",
            order=1,
            status="published"
        )
        
        # Create sample service
        self.service = Service.objects.create(
            title="CNC Cutting",
            icon="fa-scissors",
            short_description="CNC profiling and cutting.",
            detailed_description="High precision cutting details.",
            order=1,
            status="published"
        )

        # Create sample testimonial
        self.testimonial = Testimonial.objects.create(
            name="Rajesh Kumar",
            designation="Tata Power PM",
            review="Excellent B2B delivery!",
            rating=5,
            is_featured=True
        )

    def test_pages_routing_success(self):
        """Verify that all active B2B routes load successfully (status 200)."""
        client = Client()
        pages = [
            'home', 'about', 'products', 'manufacturing', 'services', 
            'gallery', 'certificates', 'testimonials', 'contact', 
            'privacy_policy', 'terms'
        ]
        for page in pages:
            response = client.get(reverse(page))
            self.assertEqual(response.status_code, 200, f"Page {page} failed to load.")

    def test_product_detail_routing(self):
        """Verify dynamic slug-based product details load correctly."""
        client = Client()
        response = client.get(reverse('product_detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.title)

    def test_form_validation_valid(self):
        """Verify the ContactRequestForm accepts valid B2B information."""
        form_data = {
            'name': 'Ramesh Sharma',
            'company_name': 'Tata Projects Ltd',
            'phone': '9988776655',
            'email': 'procurement@tata.com',
            'product': 'Tower Cross Arm',
            'quantity': 500,
            'message': 'Need customized angle punch spacings matching blueprint.'
        }
        form = ContactRequestForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_validation_invalid_phone(self):
        """Verify the ContactRequestForm rejects invalid phone numbers."""
        form_data = {
            'name': 'Ramesh',
            'company_name': 'Tata Projects',
            'phone': '9988abc655', # letters
            'email': 'procurement@tata.com',
            'product': 'Tower Cross Arm',
            'quantity': 500,
            'message': 'Test message.'
        }
        form = ContactRequestForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_contact_submission_saves_in_db(self):
        """Verify B2B form submissions insert records into the database."""
        client = Client()
        post_data = {
            'name': 'Amit Singh',
            'company_name': 'L&T Infrastructure',
            'phone': '9876543210',
            'email': 'amit@lninfra.com',
            'product': 'Tower Cross Arm',
            'quantity': 250,
            'message': 'Requesting technical quotation for 250 cross arms.'
        }
        response = client.post(reverse('home'), post_data)
        self.assertEqual(response.status_code, 302)  # redirects on success
        
        # Verify db insert
        requests = ContactRequest.objects.filter(name='Amit Singh')
        self.assertEqual(requests.count(), 1)
        self.assertEqual(requests.first().company_name, 'L&T Infrastructure')
        self.assertEqual(requests.first().quantity, 250)

    def test_seo_sitemap_xml(self):
        """Verify that sitemap.xml loads."""
        client = Client()
        response = client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/xml')

    def test_seo_robots_txt(self):
        """Verify that robots.txt is active."""
        client = Client()
        response = client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/plain')

    def test_quick_inquiry_without_message_ajax(self):
        """Verify Quick Inquiry form works via AJAX even without entering a message."""
        client = Client()
        post_data = {
            'name': 'Rahul Kumawat',
            'company_name': 'codedesk',
            'phone': '9856485756',
            'email': 'rahulkumawar6@gmail.com',
            'product': 'Cross Arm',
            'quantity': 100,
            'message': ''
        }
        response = client.post(reverse('home'), post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        
        # Verify stored contact request
        req = ContactRequest.objects.get(name='Rahul Kumawat')
        self.assertEqual(req.company_name, 'codedesk')
        self.assertEqual(req.phone, '9856485756')
        self.assertEqual(req.quantity, 100)
        self.assertTrue('Quick inquiry' in req.message)

    def test_phone_sanitization(self):
        """Verify phone numbers with country code or spaces are sanitized and accepted."""
        form_data = {
            'name': 'Test User',
            'company_name': 'Sample Corp',
            'phone': '+91 99292 58781',
            'email': '',
            'product': 'Stay Set',
            'quantity': 50,
            'message': ''
        }
        form = ContactRequestForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['phone'], '9929258781')

