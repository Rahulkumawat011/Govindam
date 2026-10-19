# Govindam Enterprises Website - Django 5

A production-ready, fully responsive, and SEO-optimized website built with Python Django 5 and Bootstrap 5 for **Govindam Enterprises** (Tawar Cross Farm & Bijli Board Related Services).

---

## Technical Stack
- **Backend**: Python Django 5.0 (runs inside Python 3.11 virtual environment)
- **Database**: SQLite (development), fully configured for MySQL migration compatibility
- **Frontend**: HTML5, CSS3 (Vanilla Custom Theme), Bootstrap 5, FontAwesome 6, AOS (Animate On Scroll) Animations, Swiper Slider, SweetAlert2 (AJAX Form alerts)
- **Utilities**: `python-dotenv` (security & environment settings), `pillow` (media management), `django-cleanup` (automatic media deletion)

---

## Features
1. **Interactive Landings**: Sticky blurring header, floating quick WhatsApp & Call actions, responsive sidebar mobile drawers.
2. **Dynamic Request Forms**: Custom validations on mobile numbers (`^[6-9]\d{9}$`), spinner loaders, and non-blocking asynchronous email notifications thread setups.
3. **Admin Dashboard**: Subclassed `AdminSite` index displaying key summary counts (Pending Leads, Total Submissions, Services, Documents) alongside export actions (Contact requests to CSV).
4. **Interactive Filters**: Document application search and gallery lightbox filtering.
5. **SEO Ready**: Dynamic `sitemap.xml` routes, custom `robots.txt` templates, JSON-LD Schema structures, Open Graph tags, and customized page title meta tags.

---

## Installation & Running Locally

### 1. Prerequisites
- Python 3.11+
- Virtual environment support

### 2. Environment Setup
Create a virtual environment and install the required dependencies:
```bash
# Verify Python version
/opt/homebrew/bin/python3.11 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Migrations & Database Setup
Initialize the database tables and apply default schemas:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Seeding Professional Dummy Data
Seed the database with default services, dynamic documents, featured testimonials, and create an admin superuser account:
```bash
python seed_data.py
```
*Seeded Admin Credentials:*
- **Username**: `admin`
- **Password**: `admin123`

### 5. Start Development Server
Run the local host environment:
```bash
python manage.py runserver
```
Visit the local endpoints:
- Website: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Admin Panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Running Automated Tests
To run unit and integration tests checking sitemaps, model choices validation, forms, and pages routing:
```bash
python manage.py test
```
