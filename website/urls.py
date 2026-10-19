from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('manufacturing/', views.manufacturing, name='manufacturing'),
    path('gallery/', views.gallery, name='gallery'),
    path('certificates/', views.certificates, name='certificates'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms'),
]
