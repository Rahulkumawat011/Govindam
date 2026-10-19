import os
import django

# Configure Django settings environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'govindam.settings')
django.setup()

from django.core.files import File
from website.models import Service, Product, Gallery, Testimonial
from django.contrib.auth.models import User
from PIL import Image
import io

def create_dummy_image(color, filename):
    """Generate a tiny solid color PNG image in memory for media uploads."""
    img = Image.new('RGB', (400, 300), color=color)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return File(img_byte_arr, name=filename)

def seed_database():
    print("Starting B2B database seeding (excluding Projects, Downloads, and Blogs)...")
    
    # 1. Create superuser if not exists
    if not User.objects.filter(username='admin').exists():
        print("Creating superuser admin/admin123...")
        User.objects.create_superuser('admin', 'admin@govindamenterprises.com', 'admin123')
    
    # Clean previous data to prevent duplicates
    Service.objects.all().delete()
    Product.objects.all().delete()
    Gallery.objects.all().delete()
    Testimonial.objects.all().delete()

    # 2. Seed 10 B2B Products
    print("Seeding 10 Products...")
    products_data = [
        {
            'title': 'Transmission Tower',
            'desc': 'We manufacture all types of Transmission Towers and Lattice Towers for high-voltage power lines.',
            'detail': 'We manufacture all types of Lattice Transmission Towers (including suspension towers, tension towers, angle towers, and terminal towers) using high-strength structural steel angles. Our structures comply with power grid and state electricity utility standard ratings. All sections are hot-dip galvanized to ensure long life against environmental corrosion.',
            'specs': 'Tower Types: Lattice Towers, Bracing Members, Support Gantries\nRaw Material: IS 2062 Structural Steel\nGalvanization Standard: IS 2629 / BS EN ISO 1461\nZinc Coating Thickness: 85 Microns minimum\nTensile Strength: 410 MPa',
            'dim': 'Custom fabricated to drawing height & loadings',
            'mat': 'Structural Steel IS 2062 Grade-A',
            'apps': 'Overhead Transmission Towers\nHigh-Voltage Grid Lines\nDistribution Sub-stations',
            'order': 1,
            'color': '#0b2e59'
        },
        {
            'title': 'Cross Arm',
            'desc': 'We manufacture all types of V-shape and straight cross arms for distribution poles.',
            'detail': 'We manufacture all types of Pole Cross Arms (V-Shape Cross Arms, straight Channel Cross Arms, F-Clamps, U-clevis cross arms, and pole-mounting fittings) for 11KV and 33KV power distribution poles. Custom configurations are available based on drawings from regional state electricity boards.',
            'specs': 'Galvanization: Hot-Dip Galvanized\nForming: CNC Punched & Sheared\nWelding Standard: MIG certified',
            'dim': '75x40 mm Channel / 65x65x6 mm Angle',
            'mat': 'Mild Steel Channel & Angle',
            'apps': '11KV/33KV Distribution Lines\nRural Grid Expansion\nUtility Poles Fitting',
            'order': 2,
            'color': '#c5a059'
        },
        {
            'title': 'Stay Set',
            'desc': 'Heavy-duty stay rod assemblies with bow, plate, and turnbuckle.',
            'detail': 'Stay Sets are crucial for securing utility poles against ground tension. Our sets include the stay rod, stay bow, anchor plate, and turnbuckle. All parts are galvanized to withstand soil corrosion.',
            'specs': 'Rod Diameter: 16mm / 20mm / 24mm\nPlate Size: 300x300x6 mm\nStandard: IS 3063 / IS 2062',
            'dim': 'Length: 1.8 Meters / 2.4 Meters',
            'mat': 'Hot Dip Galvanized Rod Steel',
            'apps': 'Line Tension Anchoring\nUtility Pole Bracing\nHigh Wind Load Stabilization',
            'order': 3,
            'color': '#2b5876'
        },
        {
            'title': 'Clamps',
            'desc': 'Heavy-duty D-clamps, PG clamps, suspension clamps, and tension clamps.',
            'detail': 'Precision engineered clamps for anchoring conductor wires to insulators or structural cross arms. We manufacture PG clamps, strain clamps, suspension clamps, and customized pole-mounting clamps.',
            'specs': 'Coating: Hot Dip Galvanized or Zinc Electroplated\nBolt Grade: High tensile 8.8 grade',
            'dim': 'Custom sizes for AAC/ACSR conductors',
            'mat': 'Forged Steel & Mild Steel Plates',
            'apps': 'Conductor Attachment\nInsulator String Mounting\nPole Clamping Assemblies',
            'order': 4,
            'color': '#141e30'
        },
        {
            'title': 'Brackets',
            'desc': 'Wall-mounting and pole-mounting transformer bracket structures.',
            'detail': 'Heavy structural steel brackets engineered for supporting pole-mounted distribution transformers. Designed to carry weights up to 5 Metric Tons safely.',
            'specs': 'Welding: Certified MIG / CO2 welding\nTesting: Load capacity tested',
            'dim': 'Custom manufactured to transformer rating',
            'mat': 'IS 2062 Channel & Plates',
            'apps': 'Distribution Transformer Mounting\nUtility Substation Fittings\nHeavy Equipment Support',
            'order': 5,
            'color': '#0f2027'
        },
        {
            'title': 'Channels',
            'desc': 'Punched and fabricated steel channels for structural frameworks.',
            'detail': 'High-precision punched structural steel channels used in sub-station frames and overhead line fittings. Manufactured with automated CNC punching machines to ensure accurate hole spacings.',
            'specs': 'Punching: CNC auto punching\nStandard lengths: 3 Meters to 6 Meters',
            'dim': 'MC 75, MC 100, MC 150',
            'mat': 'Mild Steel Channel IS 2062',
            'apps': 'Substation Structure Frames\nBase Frame Assemblies\nDistribution Line Fittings',
            'order': 6,
            'color': '#e65c00'
        },
        {
            'title': 'Angles',
            'desc': 'Fabricated structural angle irons for grid substations.',
            'detail': 'Fabricated structural angle sections sheared, punched, and galvanized. Widely used for creating bracing, frames, and support brackets in electricity board grid substations.',
            'specs': 'Angles standard: IS 808 / IS 2062\nZinc coating: Meets BS EN ISO 1461',
            'dim': '50x50x6 mm to 100x100x10 mm',
            'mat': 'Hot Dip Galvanized Angle Steel',
            'apps': 'Electrical Substation Bracing\nTower Body Sections\nStructural Support Framing',
            'order': 7,
            'color': '#3a7bd5'
        },
        {
            'title': 'Substation Gantries & MS Structures',
            'desc': 'We manufacture all types of Substation Gantries and heavy mild steel structural frameworks.',
            'detail': 'We manufacture all types of custom substation gantries, equipment support columns, transformer mounting frames, and structural MS frameworks. All fabrications are layout pre-fit tested at our Jaipur facility to ensure exact alignment with regional utility drawing details.',
            'specs': 'Structure Types: Substation Gantries, Transformer Support Frames, Equipment Mounts\nMaterial Standard: IS 2062 Structural Steel\nZinc Bath Standard: IS 2629 / BS EN ISO 1461\nWelding Standard: Certified MIG / CO2 arc welding',
            'dim': 'Fabricated to customized project drawing specs',
            'mat': 'Mild Steel Angle, Channels, Plates & Lattice Sections',
            'apps': 'Electrical Grid Stations\nPower Utility switchyards\nIndustrial Transformer Installations',
            'order': 8,
            'color': '#1d976c'
        },
        {
            'title': 'Steel Fabrication',
            'desc': 'Custom heavy steel fabrication for B2B infrastructure projects.',
            'detail': 'Heavy metal fabrication services including plate shearing, CNC bending, and automatic profile cutting. We construct steel assemblies for warehouses, metro, and rail grid infrastructure.',
            'specs': 'Bending limit: Up to 12mm thickness plate\nInspection: DPI and Ultrasonic weld checks',
            'dim': 'Varied custom specifications',
            'mat': 'Mild Steel & High-Tensile Steel Plates',
            'apps': 'Infrastructure Civil Projects\nB2B Heavy Machinery Assemblies\nRailways Overhead Structures',
            'order': 9,
            'color': '#3a6073'
        },
        {
            'title': 'Custom Fabrication',
            'desc': 'Bespoke steel components manufactured to custom drawing blueprints.',
            'detail': 'We deliver bespoke engineering solutions, fabricating specialized brackets, baseplates, clamps, and fixtures matching client engineering CAD blueprints.',
            'specs': 'Tolerance: Within +/- 0.5mm limit\nCAD Support: DWG, DXF drawing formats',
            'dim': 'Completely custom tailored',
            'mat': 'Mild Steel, Stainless Steel, Galvanized Steel',
            'apps': 'EPC Contractor Job Works\nSpecialized Solar Panel Mountings\nPrototype Machinery Assemblies',
            'order': 10,
            'color': '#203a43'
        }
    ]

    for p_idx, p in enumerate(products_data):
        prod = Product.objects.create(
            title=p['title'],
            short_description=p['desc'],
            detailed_description=p['detail'],
            specifications=p['specs'],
            dimensions=p['dim'],
            material=p['mat'],
            applications=p['apps'],
            order=p['order'],
            status='published'
        )
        if p['title'] == 'Transmission Tower' and os.path.exists('static/images/transmission_tower.jpg'):
            with open('static/images/transmission_tower.jpg', 'rb') as f:
                prod.image.save('transmission_tower.jpg', File(f), save=True)
        elif p['title'] == 'Cross Arm' and os.path.exists('static/images/cross_arm_category.jpg'):
            with open('static/images/cross_arm_category.jpg', 'rb') as f:
                prod.image.save('cross_arm_category.jpg', File(f), save=True)
        else:
            dummy_img = create_dummy_image(p['color'], f"product_{p_idx}.png")
            prod.image.save(f"product_{p_idx}.png", dummy_img, save=True)

    # 3. Seed 6 Services
    print("Seeding 6 Services...")
    services_data = [
        {
            'title': 'Steel Fabrication',
            'icon': 'fa-hammer',
            'short_desc': 'Heavy and light structural steel fabrication matching strict ISO and drawing specifications.',
            'detailed_desc': 'Our custom steel fabrication service offers high-precision structural assemblies including frames, plates, and fittings. We use automatic shearing and punching systems, certified welding stations, and full quality inspections to ensure all structural items are delivered defect-free.',
            'order': 1,
            'color': '#0b2e59'
        },
        {
            'title': 'CNC Cutting',
            'icon': 'fa-microchip',
            'short_desc': 'CNC profiling, routing, and drilling services for sheet metal and structural members.',
            'detailed_desc': 'We offer automated CNC punching, shearing, and drilling on heavy channels, angles, and plates. Our machinery operates directly on CAD layout drawings (DWG/DXF), yielding consistent bolt-hole alignments for fast structural pre-assembly.',
            'order': 2,
            'color': '#c5a059'
        },
        {
            'title': 'Plasma Cutting',
            'icon': 'fa-circle-dot',
            'short_desc': 'High-definition CNC plasma profiling for heavy mild steel plates up to 30mm thick.',
            'detailed_desc': 'CNC plasma cutting allows high-speed contour cutting of structural steel sheets. Ideal for manufacturing baseplates, gusset plates, flange rings, and mounting brackets for industrial transformers.',
            'order': 3,
            'color': '#2b5876'
        },
        {
            'title': 'Laser Cutting',
            'icon': 'fa-wand-magic-sparkles',
            'short_desc': 'Fiber laser cutting for precise sheet metal profiling with clean edges and zero burrs.',
            'detailed_desc': 'Our fiber laser cutting machines operate with high speed and precision. We cut detailed patterns, fine holes, and slots in mild steel, stainless steel, and aluminum plates, delivering perfect surface finishes.',
            'order': 4,
            'color': '#141e30'
        },
        {
            'title': 'Electrical Hardware',
            'icon': 'fa-tower-cell',
            'short_desc': 'High-volume production of state-approved transmission and distribution pole fittings.',
            'detailed_desc': 'We are high-volume suppliers of D-clamps, stay sets, anchor plates, cross arms, and pole clamps. We strictly comply with state electricity discoms and power grid corporation testing rules.',
            'order': 5,
            'color': '#0f2027'
        },
        {
            'title': 'Job Work',
            'icon': 'fa-screwdriver-wrench',
            'short_desc': 'Contract shearing, punching, bending, and galvanizing services on client-supplied steel.',
            'detailed_desc': 'We offer comprehensive custom job works. Bring your raw steel sections, and we punch, shear, bend, assemble, and hot-dip galvanize them to your technical specifications.',
            'order': 6,
            'color': '#e65c00'
        }
    ]

    for s_idx, s in enumerate(services_data):
        dummy_img = create_dummy_image(s['color'], f"service_{s_idx}.png")
        service = Service.objects.create(
            title=s['title'],
            icon=s['icon'],
            short_description=s['short_desc'],
            detailed_description=s['detailed_desc'],
            order=s['order'],
            status='published'
        )
        service.image.save(f"service_{s_idx}.png", dummy_img, save=True)

    # 4. Seed Gallery Items (6 items matching the new categorized tags)
    print("Seeding Gallery...")
    gallery_data = [
        {'title': 'Jaipur Factory Fabrication Shop', 'cat': 'factory', 'color': '#2b5876'},
        {'title': 'CNC Fiber Laser Cutter Operational', 'cat': 'machines', 'color': '#141e30'},
        {'title': 'Finished Tower Cross Arms Stacked', 'cat': 'products', 'color': '#0f2027'},
        {'title': 'Hot Dip Galvanizing Bath Process', 'cat': 'manufacturing', 'color': '#e65c00'},
        {'title': 'Ready-to-Ship Stay Sets Packed', 'cat': 'dispatch', 'color': '#3a7bd5'},
        {'title': 'Substation Structure Installation', 'cat': 'installation', 'color': '#1d976c'}
    ]

    for g_idx, g in enumerate(gallery_data):
        dummy_img = create_dummy_image(g['color'], f"gallery_{g_idx}.png")
        gal = Gallery.objects.create(
            title=g['title'],
            category=g['cat']
        )
        gal.image.save(f"gallery_{g_idx}.png", dummy_img, save=True)

    # 5. Seed Testimonials (4 Items)
    print("Seeding Testimonials...")
    testimonials_data = [
        {'name': 'Rajesh Kumar', 'role': 'Lead Project Manager - Tata Power', 'rating': 5, 'text': 'Govindam Enterprises delivered 80 tons of cross arms under tight schedule parameters. The HDG zinc coating thickness was flawless and passed discom tests easily.', 'color': '#f8d7da'},
        {'name': 'Sunil Verma', 'role': 'Procurement Head - Adani Solar', 'rating': 5, 'text': 'High quality stay set assemblies and clamps. Their CNC cutting precision is exceptional, fitting our custom mounting arrays perfectly.', 'color': '#d1e7dd'},
        {'name': 'Pooja Sharma', 'role': 'Contractor - L&T Infra', 'rating': 5, 'text': 'Excellent liaisoning and custom job work services. They have robust factory machinery capability and competitive B2B prices.', 'color': '#fff3cd'},
        {'name': 'Amit Singh', 'role': 'Director - Rajasthan Solar Gids', 'rating': 5, 'text': 'Highly professional fabrication. Their ISO 9001:2015 standards are visible in the dimensional tolerances. A reliable transmission partner.', 'color': '#cff4fc'}
    ]

    for t_idx, t in enumerate(testimonials_data):
        dummy_img = create_dummy_image(t['color'], f"avatar_{t_idx}.png")
        t_obj = Testimonial.objects.create(
            name=t['name'],
            designation=t['role'],
            review=t['text'],
            rating=t['rating'],
            is_featured=True
        )
        t_obj.image.save(f"avatar_{t_idx}.png", dummy_img, save=True)

    print("B2B Database seeding completed successfully!")

if __name__ == '__main__':
    seed_database()
