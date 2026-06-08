import re
import csv
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User as DjangoUser
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from .models import (
    Inquiry, Product, Testimonial,
    Customer, Order, Appointment,
    Prescription, ProductReview, WishlistItem,  # NEW
)

# ─── Business Info ────────────────────────────────────────────────────────────

BUSINESS_INFO = {
    'business_name': 'Eye Drishti Optical',
    'tagline': 'Clear Vision, Better Life | साफ दृष्टि, बेहतर जीवन',
    'phone': '+91 90447 90354',
    'whatsapp': '919044790354',
    'address': 'Shop No. 6, Nayab Market, Kachahri Road, Near SBI Bank, Pratapgarh, U.P. 230001',
    'hours': 'Mon–Sat: 10:00 AM – 8:00 PM',
    'closed': 'Closed on Sundays',
    'rating': '4.7',
    'reviews_count': '120+',
    'years_experience': '10+',
    'customers_served': '5000+',
    'google_maps_embed': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3601.4!2d81.9833!3d25.9167!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMjXCsDU1JzAwLjAiTiA4McKwNTknMDAuMCJF!5e0!3m2!1sen!2sin!4v1620000000000!5m2!1sen!2sin',
    'shop_images': [
        'https://lh3.googleusercontent.com/p/AF1QipO_2KA4pgDybf0IXeDJJ5yFowTThMo1ETgSeSkY=s1360-w1360-h1020-rw',
        'https://lh3.googleusercontent.com/p/AF1QipPKBIW5lNc_RoVZzdl6rH4IfJGqdDS5qJVrQQ4M=s1360-w1360-h1020-rw',
    ],
}

DEFAULT_PRODUCTS = [
    {'id': 'dp_1', 'name': 'Imp Classic Frame', 'category': 'eyeglasses', 'description': 'Durable and stylish classic frames perfect for everyday use. Lightweight design for all-day comfort.', 'price_range': '₹599 – ₹1,499', 'image_url': 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=600&q=80', 'brand': 'Imp', 'is_featured': True},
    {'id': 'dp_2', 'name': 'EMENITY Blue Light Glasses', 'category': 'eyeglasses', 'description': 'Anti-blue light lenses ideal for screen time. Reduces eye strain from mobile and computer use.', 'price_range': '₹799 – ₹1,999', 'image_url': 'https://images.unsplash.com/photo-1508296695146-257a814070b4?w=600&q=80', 'brand': 'Emenity', 'is_featured': True},
    {'id': 'dp_3', 'name': 'HUFF LINE Metal Frame', 'category': 'frames', 'description': 'Premium metal frames with ultra-thin profile. Sophisticated look for professionals and students.', 'price_range': '₹899 – ₹2,499', 'image_url': 'https://images.unsplash.com/photo-1591076482161-42ce6da69f67?w=600&q=80', 'brand': 'Huff Line', 'is_featured': True},
    {'id': 'dp_4', 'name': 'Rimless Titanium', 'category': 'frames', 'description': 'Ultra-lightweight rimless frames made from pure titanium. Barely noticeable, maximum comfort.', 'price_range': '₹1,299 – ₹3,499', 'image_url': 'https://images.unsplash.com/photo-1512909006721-3d6018887383?w=600&q=80', 'brand': 'Drishti Premium', 'is_featured': True},
    {'id': 'dp_5', 'name': 'Aviator Sunglasses', 'category': 'sunglasses', 'description': 'Classic aviator style with 100% UV400 protection. Perfect for outdoor activities and driving.', 'price_range': '₹399 – ₹1,299', 'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=600&q=80', 'brand': 'SunShield', 'is_featured': False},
    {'id': 'dp_6', 'name': 'Acuvue Contact Lenses', 'category': 'contact_lenses', 'description': 'Daily disposable contact lenses for sharp, clear vision. Comfortable for sensitive eyes.', 'price_range': '₹450 – ₹1,800 / box', 'image_url': 'https://images.unsplash.com/photo-1585435557343-3b092031a831?w=600&q=80', 'brand': 'Acuvue', 'is_featured': False},
    {'id': 'dp_7', 'name': 'Reading Glasses +1.0 to +3.5', 'category': 'reading_glasses', 'description': 'Affordable reading glasses for presbyopia. Available in multiple magnification strengths.', 'price_range': '₹199 – ₹599', 'image_url': 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=600&q=80', 'brand': 'ReadEase', 'is_featured': False},
    {'id': 'dp_8', 'name': 'Cat Eye Fashion Frames', 'category': 'eyeglasses', 'description': 'Trendy cat eye frames for women. Bold style that complements every face shape.', 'price_range': '₹699 – ₹1,799', 'image_url': 'https://images.unsplash.com/photo-1556306535-0f09a537f0a3?w=600&q=80', 'brand': 'FashionEye', 'is_featured': False},
]

DEFAULT_TESTIMONIALS = [
    {'customer_name': 'Rahul Sharma', 'rating': 5, 'review': 'Bahut achha service mila! Eye test free tha aur glasses bhi jaldi mil gayi. Drishti Optical se main bahut khush hoon.', 'location': 'Pratapgarh'},
    {'customer_name': 'Sunita Devi', 'rating': 5, 'review': 'Maine yahan se chashma banwaya. Price bahut reasonable hai aur quality bhi top class. Doctor sahab ne bahut dhyan se check kiya.', 'location': 'Bela, Pratapgarh'},
    {'customer_name': 'Amit Kumar', 'rating': 4, 'review': 'Good collection of frames at affordable prices. The staff is very helpful and friendly. My whole family gets their glasses from here.', 'location': 'Kunda, Pratapgarh'},
    {'customer_name': 'Priya Singh', 'rating': 5, 'review': 'Excellent eye checkup facility. Got my spectacles within same day. The lenses quality is superb. Very happy with their service.', 'location': 'Pratapgarh City'},
]

FAQS = [
    {'question': 'Do you offer free eye tests?', 'answer': 'Yes! Free basic eye checkup with every frame purchase. Comprehensive eye examination at ₹50.'},
    {'question': 'Which brands are available?', 'answer': 'Imp, Emenity, Huff Line, Acuvue, Ray-Ban, and many more. Frames from ₹199.'},
    {'question': 'How long does it take to prepare glasses?', 'answer': 'Most standard prescriptions ready within 1–2 hours. Complex lenses: 1–2 days.'},
    {'question': 'Do you provide home delivery?', 'answer': 'Yes, home delivery within Pratapgarh city and nearby areas.'},
    {'question': 'What is your return/exchange policy?', 'answer': "7-day exchange on frames. Lens re-make free within 30 days if prescription doesn't suit."},
    {'question': 'Do you repair old glasses?', 'answer': 'Yes! We repair broken frames, replace nose pads, tighten screws. Very affordable charges.'},
    {'question': 'Can I see my eye prescription online?', 'answer': 'Yes! After your eye checkup at our shop, your prescription is saved in your account. Login to view it anytime.'},
    {'question': 'Is there a referral program?', 'answer': 'Yes! Share your referral code with friends. When they register, both of you get a discount on your next purchase.'},
]

SERVICES = [
    {'icon': '👁️', 'title': 'Free Eye Checkup', 'title_hi': 'मुफ्त आंख जांच', 'description': 'Comprehensive eye examination by trained optician.', 'highlight': 'FREE with frame purchase'},
    {'icon': '🔬', 'title': 'Lens Fitting & Coating', 'title_hi': 'लेंस फिटिंग', 'description': 'Anti-reflection, blue-cut, photochromic, and bifocal lenses.', 'highlight': 'All types available'},
    {'icon': '🔧', 'title': 'Frame Repair', 'title_hi': 'फ्रेम मरम्मत', 'description': 'Quick repair of broken frames, hinges, nose pads, and screws.', 'highlight': 'Same day service'},
    {'icon': '📋', 'title': 'Power Prescription', 'title_hi': 'पावर परीक्षण', 'description': 'Accurate power testing for near, distance, and reading vision.', 'highlight': 'Digital accuracy'},
    {'icon': '👓', 'title': 'Contact Lens Fitting', 'title_hi': 'कॉन्टैक्ट लेंस', 'description': 'Expert fitting and training for contact lenses.', 'highlight': 'All types stocked'},
    {'icon': '🏠', 'title': 'Home Delivery', 'title_hi': 'होम डिलीवरी', 'description': 'Get your glasses delivered at your doorstep in Pratapgarh.', 'highlight': 'Pratapgarh & nearby'},
]

LENS_TYPES = ['Single Vision', 'Bifocal', 'Progressive', 'Blue Cut', 'Photochromic', 'Bifocal + Blue Cut']
LENS_COATINGS = ['Anti-Reflection (AR)', 'UV400', 'Scratch Resistant', 'Photochromic', 'Mirror Coating', 'No Coating']
FRAME_COLORS = ['Black', 'Silver', 'Gold', 'Brown', 'Blue', 'Red', 'Transparent', 'Gunmetal']

MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 15 * 60


def _check_rate_limit(request):
    attempts = request.session.get('login_attempts', 0)
    lockout_until = request.session.get('login_lockout_until', 0)
    now = time.time()
    if lockout_until and now < lockout_until:
        return True, int(lockout_until - now)
    if lockout_until and now >= lockout_until:
        request.session['login_attempts'] = 0
        request.session['login_lockout_until'] = 0
    return False, 0


def _record_failed_attempt(request):
    attempts = request.session.get('login_attempts', 0) + 1
    request.session['login_attempts'] = attempts
    if attempts >= MAX_LOGIN_ATTEMPTS:
        request.session['login_lockout_until'] = time.time() + LOCKOUT_DURATION
    return attempts


def _reset_rate_limit(request):
    request.session['login_attempts'] = 0
    request.session['login_lockout_until'] = 0


def _validate_phone(phone):
    phone = re.sub(r'[\s\-\(\)+]', '', phone)
    if phone.startswith('91') and len(phone) == 12:
        phone = phone[2:]
    if not phone:
        return False, '❌ Phone number is required.'
    if not re.match(r'^[6-9]\d{9}$', phone):
        return False, '❌ Enter a valid 10-digit Indian mobile number (starting with 6–9).'
    return True, phone


def _no_cache(response):
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


def protected_render(request, template, context):
    return _no_cache(render(request, template, context))


def get_logged_in_customer(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return None
    try:
        return Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        del request.session['customer_id']
        return None


def _base_context(request):
    ctx = dict(BUSINESS_INFO)
    ctx['customer'] = get_logged_in_customer(request)
    return ctx


def _get_wishlist_ids(request):
    """Return set of product_id_str values in current customer's wishlist."""
    customer = get_logged_in_customer(request)
    if not customer:
        return set()
    return set(WishlistItem.objects.filter(customer=customer).values_list('product_id_str', flat=True))


# ─── Public Views ─────────────────────────────────────────────────────────────

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        message_text = request.POST.get('message', '').strip()

        if name and phone and message_text:
            Inquiry.objects.create(
                name=name, phone=phone,
                email=email if email else None,
                message=message_text,
            )
            messages.success(request, f'✅ Shukriya {name} ji! Aapka message mil gaya. Hum jald hi aapse contact karenge.')
        else:
            messages.error(request, '❌ Please fill Name, Phone and Message fields.')
        return redirect('home')

    db_products = list(Product.objects.all())
    use_db = bool(db_products)
    products_list = db_products if use_db else DEFAULT_PRODUCTS

    db_testimonials = list(Testimonial.objects.filter(is_active=True))
    testimonials = db_testimonials if db_testimonials else DEFAULT_TESTIMONIALS

    featured = (
        list(Product.objects.filter(is_featured=True))
        if use_db
        else [p for p in products_list if p.get('is_featured')]
    )

    context = {
        **_base_context(request),
        'products': products_list,
        'featured_products': featured[:4],
        'testimonials': testimonials,
        'faqs': FAQS,
        'services': SERVICES,
        'use_db_products': use_db,
        'categories': ['eyeglasses', 'sunglasses', 'contact_lenses', 'frames', 'reading_glasses'],
        'wishlist_ids': _get_wishlist_ids(request),
    }
    return render(request, 'optical/home.html', context)


def products(request):
    category = request.GET.get('category', '')
    db_products = list(Product.objects.all())
    use_db = bool(db_products)
    all_products = db_products if use_db else DEFAULT_PRODUCTS

    if category and use_db:
        filtered = list(Product.objects.filter(category=category))
    elif category:
        filtered = [p for p in all_products if p.get('category') == category]
    else:
        filtered = all_products

    context = {
        **_base_context(request),
        'products': filtered,
        'all_products': all_products,
        'selected_category': category,
        'categories': ['eyeglasses', 'sunglasses', 'contact_lenses', 'frames', 'reading_glasses'],
        'use_db_products': use_db,
        'wishlist_ids': _get_wishlist_ids(request),
    }
    return render(request, 'optical/products.html', context)


# ─── Auth Views ───────────────────────────────────────────────────────────────

def customer_login(request):
    if get_logged_in_customer(request):
        return _no_cache(redirect('home'))
    if request.user.is_authenticated and request.user.is_staff:
        return _no_cache(redirect('admin_dashboard'))

    next_url = request.GET.get('next', '')
    referral_code = request.GET.get('ref', '').upper().strip()  # NEW: referral code pre-fill

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'signup':
            name = request.POST.get('name', '').strip()
            phone_raw = request.POST.get('phone', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')
            ref_code = request.POST.get('referral_code', '').strip().upper()  # NEW

            phone_valid, phone_result = _validate_phone(phone_raw)

            referred_by = None
            if ref_code:
                try:
                    referred_by = Customer.objects.get(referral_code=ref_code)
                except Customer.DoesNotExist:
                    messages.error(request, '❌ Invalid referral code. Leave blank if you don\'t have one.')
                    context = {**_base_context(request), 'next': next_url, 'ref': ref_code}
                    return _no_cache(render(request, 'optical/login.html', context))

            if not all([name, phone_raw, password]):
                messages.error(request, '❌ Name, Phone and Password are required.')
            elif len(name) < 2:
                messages.error(request, '❌ Please enter your full name (at least 2 characters).')
            elif not phone_valid:
                messages.error(request, phone_result)
            elif email and not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
                messages.error(request, '❌ Please enter a valid email address.')
            elif len(password) < 6:
                messages.error(request, '❌ Password must be at least 6 characters.')
            elif password != confirm_password:
                messages.error(request, '❌ Passwords do not match.')
            elif Customer.objects.filter(phone=phone_result).exists():
                messages.error(request, '❌ This phone number is already registered. Please login.')
            else:
                customer = Customer.objects.create(
                    name=name,
                    phone=phone_result,
                    email=email if email else None,
                    password=make_password(password),
                    referred_by=referred_by,
                )
                request.session['customer_id'] = customer.id
                request.session.set_expiry(86400 * 7)
                _reset_rate_limit(request)
                messages.success(request, f'✅ Welcome {name} ji! Account created successfully.')
                return _no_cache(redirect(next_url or 'home'))

        elif action == 'login':
            is_locked, seconds_left = _check_rate_limit(request)
            if is_locked:
                minutes_left = (seconds_left // 60) + 1
                messages.error(request, f'🔒 Too many failed attempts. Please try again in {minutes_left} minute(s).')
                context = {**_base_context(request), 'next': next_url, 'is_locked': True, 'seconds_left': seconds_left}
                return _no_cache(render(request, 'optical/login.html', context))

            identifier = request.POST.get('phone', '').strip()
            password = request.POST.get('password', '')

            if not identifier or not password:
                messages.error(request, '❌ Phone/Username and Password cannot be empty.')
            else:
                django_user = None
                try:
                    django_user = DjangoUser.objects.get(username=identifier)
                except DjangoUser.DoesNotExist:
                    pass

                if django_user and django_user.is_staff:
                    auth_user = authenticate(request, username=identifier, password=password)
                    if auth_user and auth_user.is_staff:
                        auth_login(request, auth_user)
                        _reset_rate_limit(request)
                        display_name = auth_user.get_full_name() or auth_user.username
                        messages.success(request, f'✅ Welcome, {display_name}! (Admin)')
                        return _no_cache(redirect(next_url or 'admin_dashboard'))
                    else:
                        attempts = _record_failed_attempt(request)
                        remaining = MAX_LOGIN_ATTEMPTS - attempts
                        if remaining > 0:
                            messages.error(request, f'❌ Incorrect admin password. {remaining} attempt(s) remaining.')
                        else:
                            messages.error(request, '🔒 Too many failed attempts. Locked for 15 minutes.')
                else:
                    phone_valid, phone_result = _validate_phone(identifier)
                    if not phone_valid:
                        messages.error(request, phone_result)
                    else:
                        try:
                            customer = Customer.objects.get(phone=phone_result)
                            if check_password(password, customer.password):
                                request.session['customer_id'] = customer.id
                                request.session.set_expiry(86400 * 7)
                                _reset_rate_limit(request)
                                messages.success(request, f'✅ Welcome back, {customer.name} ji!')
                                return _no_cache(redirect(next_url or 'home'))
                            else:
                                attempts = _record_failed_attempt(request)
                                remaining = MAX_LOGIN_ATTEMPTS - attempts
                                if remaining > 0:
                                    messages.error(request, f'❌ Incorrect password. {remaining} attempt(s) remaining.')
                                else:
                                    messages.error(request, '🔒 Too many failed attempts. Locked for 15 minutes.')
                        except Customer.DoesNotExist:
                            _record_failed_attempt(request)
                            messages.error(request, '❌ No account found with this phone number. Please register.')

    context = {
        **_base_context(request),
        'next': next_url,
        'ref': referral_code,
    }
    return _no_cache(render(request, 'optical/login.html', context))


def customer_logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    request.session.flush()
    response = redirect('customer_login')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


def customer_dashboard(request):
    customer = get_logged_in_customer(request)
    if not customer:
        return redirect('/login/?next=/dashboard/')

    orders = Order.objects.filter(customer=customer).order_by('-created_at')
    appointments = Appointment.objects.filter(customer=customer).order_by('-preferred_date')
    prescriptions = Prescription.objects.filter(customer=customer).order_by('-exam_date')  # NEW
    wishlist = WishlistItem.objects.filter(customer=customer).order_by('-added_at')  # NEW
    reviews = ProductReview.objects.filter(customer=customer).order_by('-created_at')  # NEW
    referrals = Customer.objects.filter(referred_by=customer).order_by('-created_at')  # NEW

    context = {
        **_base_context(request),
        'orders': orders,
        'appointments': appointments,
        'prescriptions': prescriptions,
        'wishlist': wishlist,
        'reviews': reviews,
        'referrals': referrals,
        'referral_code': customer.referral_code,
        'referral_link': request.build_absolute_uri(f'/login/?ref={customer.referral_code}'),
    }
    return protected_render(request, 'optical/dashboard.html', context)


# NEW: Update Customer Profile
def update_profile(request):
    customer = get_logged_in_customer(request)
    if not customer:
        return redirect('/login/?next=/profile/update/')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not name or len(name) < 2:
            messages.error(request, '❌ Please enter a valid name.')
        elif email and not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
            messages.error(request, '❌ Invalid email address.')
        elif new_password and len(new_password) < 6:
            messages.error(request, '❌ New password must be at least 6 characters.')
        elif new_password and new_password != confirm_password:
            messages.error(request, '❌ Passwords do not match.')
        else:
            customer.name = name
            customer.email = email if email else None
            customer.address = address
            customer.city = city
            customer.pincode = pincode
            if new_password:
                customer.password = make_password(new_password)
            customer.save()
            messages.success(request, '✅ Profile updated successfully!')
            return redirect('customer_dashboard')

    context = {
        **_base_context(request),
        'customer': customer,
    }
    return protected_render(request, 'optical/update_profile.html', context)


# ─── Order / Buy Views ────────────────────────────────────────────────────────

def buy_product(request, product_id):
    customer = get_logged_in_customer(request)
    if not customer:
        return redirect(f'/login/?next=/buy/{product_id}/')

    db_product = None
    product_info = {}

    if str(product_id).startswith('dp_'):
        idx = int(str(product_id).replace('dp_', '')) - 1
        if 0 <= idx < len(DEFAULT_PRODUCTS):
            product_info = DEFAULT_PRODUCTS[idx]
        else:
            messages.error(request, 'Product not found.')
            return redirect('products')
    else:
        try:
            db_product = Product.objects.get(pk=product_id)
            product_info = {
                'name': db_product.name,
                'price_range': db_product.price_range,
                'image_url': db_product.image_url,
                'description': db_product.description,
                'brand': db_product.brand,
            }
        except Product.DoesNotExist:
            messages.error(request, 'Product not found.')
            return redirect('products')

    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address', '').strip()
        delivery_city = request.POST.get('delivery_city', '').strip()
        delivery_pincode = request.POST.get('delivery_pincode', '').strip()
        landmark = request.POST.get('landmark', '').strip()
        notes = request.POST.get('notes', '').strip()
        # NEW: lens customisation
        lens_type = request.POST.get('lens_type', '').strip()
        lens_coating = request.POST.get('lens_coating', '').strip()
        frame_color = request.POST.get('frame_color', '').strip()

        if not all([delivery_address, delivery_city, delivery_pincode]):
            messages.error(request, '❌ Please fill all required delivery details.')
        elif not re.match(r'^\d{6}$', delivery_pincode):
            messages.error(request, '❌ Please enter a valid 6-digit pincode.')
        else:
            order = Order.objects.create(
                customer=customer,
                product=db_product,
                product_name=product_info['name'],
                product_price_range=product_info.get('price_range', ''),
                delivery_address=delivery_address,
                delivery_city=delivery_city,
                delivery_pincode=delivery_pincode,
                landmark=landmark,
                notes=notes,
                lens_type=lens_type,
                lens_coating=lens_coating,
                frame_color=frame_color,
            )
            messages.success(
                request,
                f'✅ Order #{order.id} placed successfully! '
                f'We will contact you on {customer.phone} to confirm.'
            )
            return redirect('order_success', order_id=order.id)

    context = {
        **_base_context(request),
        'product': product_info,
        'product_id': product_id,
        'customer': customer,
        'lens_types': LENS_TYPES,
        'lens_coatings': LENS_COATINGS,
        'frame_colors': FRAME_COLORS,
    }
    return protected_render(request, 'optical/buy.html', context)


def order_success(request, order_id):
    customer = get_logged_in_customer(request)
    if not customer:
        return redirect('customer_login')

    try:
        order = Order.objects.get(id=order_id, customer=customer)
    except Order.DoesNotExist:
        return redirect('home')

    context = {
        **_base_context(request),
        'order': order,
    }
    return protected_render(request, 'optical/order_success.html', context)


# ─── Appointment Views ────────────────────────────────────────────────────────

def book_appointment(request):
    customer = get_logged_in_customer(request)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone_raw = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        service_type = request.POST.get('service_type', 'eye_checkup')
        preferred_date = request.POST.get('preferred_date', '')
        preferred_time = request.POST.get('preferred_time', '')
        notes = request.POST.get('notes', '').strip()

        phone_valid, phone_result = _validate_phone(phone_raw)

        if not all([name, phone_raw, preferred_date, preferred_time]):
            messages.error(request, '❌ Please fill all required fields.')
        elif not phone_valid:
            messages.error(request, phone_result)
        else:
            appointment = Appointment.objects.create(
                customer=customer,
                name=name,
                phone=phone_result,
                email=email if email else None,
                service_type=service_type,
                preferred_date=preferred_date,
                preferred_time=preferred_time,
                notes=notes,
            )
            messages.success(
                request,
                f'✅ Appointment booked! We will confirm on {phone_result}. '
                f'Appointment ID: #{appointment.id}'
            )
            return redirect('appointment_success', appt_id=appointment.id)

    context = {
        **_base_context(request),
        'customer': customer,
        'service_choices': Appointment.SERVICE_CHOICES,
        'time_slots': [
            '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM',
            '12:00 PM', '12:30 PM', '01:00 PM', '01:30 PM',
            '02:00 PM', '02:30 PM', '03:00 PM', '03:30 PM',
            '04:00 PM', '04:30 PM', '05:00 PM', '05:30 PM',
            '06:00 PM', '06:30 PM', '07:00 PM', '07:30 PM',
        ],
    }
    return render(request, 'optical/appointment.html', context)


def appointment_success(request, appt_id):
    try:
        appt = Appointment.objects.get(id=appt_id)
    except Appointment.DoesNotExist:
        return redirect('home')

    context = {
        **_base_context(request),
        'appointment': appt,
    }
    return render(request, 'optical/appointment_success.html', context)


# ─── NEW: Prescription View ────────────────────────────────────────────────────

def view_prescription(request, rx_id):
    """Customer can view their own prescription."""
    customer = get_logged_in_customer(request)
    if not customer:
        return redirect(f'/login/?next=/prescription/{rx_id}/')
    try:
        rx = Prescription.objects.get(id=rx_id, customer=customer)
    except Prescription.DoesNotExist:
        messages.error(request, '❌ Prescription not found.')
        return redirect('customer_dashboard')

    context = {
        **_base_context(request),
        'rx': rx,
    }
    return protected_render(request, 'optical/prescription.html', context)


# ─── NEW: Wishlist Views ──────────────────────────────────────────────────────

def toggle_wishlist(request):
    """AJAX-friendly: add/remove product from wishlist. Returns JSON."""
    customer = get_logged_in_customer(request)
    if not customer:
        return JsonResponse({'status': 'login_required'}, status=401)

    if request.method != 'POST':
        return JsonResponse({'status': 'method_not_allowed'}, status=405)

    product_id_str = request.POST.get('product_id', '').strip()
    product_name = request.POST.get('product_name', '').strip()

    if not product_id_str:
        return JsonResponse({'status': 'error', 'message': 'product_id missing'}, status=400)

    # Check if it's a DB product
    db_product = None
    if not product_id_str.startswith('dp_'):
        try:
            db_product = Product.objects.get(pk=product_id_str)
            product_name = product_name or db_product.name
        except Product.DoesNotExist:
            pass

    existing = WishlistItem.objects.filter(customer=customer, product_id_str=product_id_str).first()
    if existing:
        existing.delete()
        return JsonResponse({'status': 'removed', 'message': f'Removed from wishlist'})
    else:
        WishlistItem.objects.create(
            customer=customer,
            product=db_product,
            product_name=product_name or product_id_str,
            product_id_str=product_id_str,
        )
        return JsonResponse({'status': 'added', 'message': f'Added to wishlist'})


# ─── NEW: Product Review View ─────────────────────────────────────────────────

def submit_review(request, product_id):
    customer = get_logged_in_customer(request)
    if not customer:
        return redirect(f'/login/?next=/review/{product_id}/')

    try:
        db_product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        messages.error(request, '❌ Product not found.')
        return redirect('products')

    # Check if customer already reviewed this product
    existing = ProductReview.objects.filter(customer=customer, product=db_product).first()
    if existing:
        messages.info(request, 'ℹ️ You have already submitted a review for this product.')
        return redirect('products')

    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        review_text = request.POST.get('review', '').strip()

        if not review_text or len(review_text) < 10:
            messages.error(request, '❌ Please write a review of at least 10 characters.')
        elif rating not in range(1, 6):
            messages.error(request, '❌ Invalid rating.')
        else:
            ProductReview.objects.create(
                product=db_product,
                customer=customer,
                rating=rating,
                review=review_text,
                is_approved=False,  # Admin must approve
            )
            messages.success(request, '✅ Shukriya! Your review has been submitted and will appear after approval.')
            return redirect('customer_dashboard')

    context = {
        **_base_context(request),
        'product': db_product,
    }
    return protected_render(request, 'optical/submit_review.html', context)


# ─── Admin Dashboard View ─────────────────────────────────────────────────────

def admin_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/login/?next=/admin-dashboard/')

    order_status = request.GET.get('order_status', '')
    appt_confirmed = request.GET.get('appt_confirmed', '')
    search = request.GET.get('search', '').strip()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_order_status':
            order_id = request.POST.get('order_id')
            new_status = request.POST.get('status')
            admin_note = request.POST.get('admin_note', '').strip()  # NEW
            try:
                order = Order.objects.get(id=order_id)
                order.status = new_status
                if admin_note:
                    order.admin_note = admin_note
                order.save()
                messages.success(request, f'✅ Order #{order_id} status updated to {new_status}.')
            except Order.DoesNotExist:
                messages.error(request, '❌ Order not found.')

        elif action == 'confirm_appointment':
            appt_id = request.POST.get('appt_id')
            admin_note = request.POST.get('admin_note', '').strip()  # NEW
            try:
                appt = Appointment.objects.get(id=appt_id)
                appt.is_confirmed = True
                if admin_note:
                    appt.admin_note = admin_note
                appt.save()
                messages.success(request, f'✅ Appointment #{appt_id} confirmed.')
            except Appointment.DoesNotExist:
                messages.error(request, '❌ Appointment not found.')

        # NEW: save prescription from admin dashboard
        elif action == 'save_prescription':
            customer_id = request.POST.get('customer_id')
            exam_date = request.POST.get('exam_date')
            try:
                cust = Customer.objects.get(id=customer_id)
                Prescription.objects.create(
                    customer=cust,
                    exam_date=exam_date,
                    right_sph=request.POST.get('right_sph', ''),
                    right_cyl=request.POST.get('right_cyl', ''),
                    right_axis=request.POST.get('right_axis', ''),
                    right_add=request.POST.get('right_add', ''),
                    right_va=request.POST.get('right_va', ''),
                    left_sph=request.POST.get('left_sph', ''),
                    left_cyl=request.POST.get('left_cyl', ''),
                    left_axis=request.POST.get('left_axis', ''),
                    left_add=request.POST.get('left_add', ''),
                    left_va=request.POST.get('left_va', ''),
                    pd=request.POST.get('pd', ''),
                    notes=request.POST.get('notes', ''),
                )
                messages.success(request, f'✅ Prescription saved for {cust.name}.')
            except Customer.DoesNotExist:
                messages.error(request, '❌ Customer not found.')

        # NEW: approve product review
        elif action == 'approve_review':
            review_id = request.POST.get('review_id')
            try:
                rev = ProductReview.objects.get(id=review_id)
                rev.is_approved = True
                rev.save()
                messages.success(request, f'✅ Review #{review_id} approved.')
            except ProductReview.DoesNotExist:
                messages.error(request, '❌ Review not found.')

        elif action == 'delete_review':
            review_id = request.POST.get('review_id')
            try:
                ProductReview.objects.get(id=review_id).delete()
                messages.success(request, f'✅ Review #{review_id} deleted.')
            except ProductReview.DoesNotExist:
                pass

        qs = request.META.get('QUERY_STRING', '')
        return redirect(request.path + ('?' + qs if qs else ''))

    orders_qs = Order.objects.select_related('customer', 'product').order_by('-created_at')
    if order_status:
        orders_qs = orders_qs.filter(status=order_status)
    if search:
        orders_qs = (
            orders_qs.filter(customer__name__icontains=search) |
            orders_qs.filter(customer__phone__icontains=search) |
            orders_qs.filter(product_name__icontains=search)
        )

    appts_qs = Appointment.objects.select_related('customer').order_by('-created_at')
    if appt_confirmed == 'confirmed':
        appts_qs = appts_qs.filter(is_confirmed=True)
    elif appt_confirmed == 'pending':
        appts_qs = appts_qs.filter(is_confirmed=False)
    if search:
        appts_qs = appts_qs.filter(name__icontains=search) | appts_qs.filter(phone__icontains=search)

    customers_qs = Customer.objects.order_by('-created_at')
    if search:
        customers_qs = customers_qs.filter(name__icontains=search) | customers_qs.filter(phone__icontains=search)

    inquiries_qs = Inquiry.objects.order_by('-created_at')
    reviews_qs = ProductReview.objects.select_related('customer', 'product').order_by('-created_at')  # NEW
    prescriptions_qs = Prescription.objects.select_related('customer').order_by('-exam_date')  # NEW

    stats = {
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'confirmed_orders': Order.objects.filter(status='confirmed').count(),
        'delivered_orders': Order.objects.filter(status='delivered').count(),
        'total_appointments': Appointment.objects.count(),
        'pending_appointments': Appointment.objects.filter(is_confirmed=False).count(),
        'confirmed_appointments': Appointment.objects.filter(is_confirmed=True).count(),
        'total_customers': Customer.objects.count(),
        'total_inquiries': Inquiry.objects.count(),
        'pending_reviews': ProductReview.objects.filter(is_approved=False).count(),  # NEW
        'total_prescriptions': Prescription.objects.count(),  # NEW
    }

    context = {
        **_base_context(request),
        'orders': orders_qs,
        'appointments': appts_qs,
        'customers': customers_qs,
        'inquiries': inquiries_qs,
        'reviews': reviews_qs,
        'prescriptions': prescriptions_qs,
        'stats': stats,
        'order_status_filter': order_status,
        'appt_confirmed_filter': appt_confirmed,
        'search': search,
        'order_status_choices': Order.STATUS_CHOICES,
    }
    return protected_render(request, 'optical/admin_dashboard.html', context)


# ─── NEW: CSV Export Views ─────────────────────────────────────────────────────

def export_orders_csv(request):
    """Admin-only: export all orders as CSV."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/login/')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Order ID', 'Customer Name', 'Phone', 'Product', 'Price Range',
        'Lens Type', 'Lens Coating', 'Frame Color',
        'Address', 'City', 'Pincode', 'Landmark',
        'Status', 'Notes', 'Admin Note', 'Date'
    ])
    for order in Order.objects.select_related('customer').order_by('-created_at'):
        writer.writerow([
            order.id, order.customer.name, order.customer.phone,
            order.product_name, order.product_price_range,
            order.lens_type, order.lens_coating, order.frame_color,
            order.delivery_address, order.delivery_city, order.delivery_pincode,
            order.landmark, order.status, order.notes, order.admin_note,
            order.created_at.strftime('%d/%m/%Y %H:%M'),
        ])
    return response


def export_customers_csv(request):
    """Admin-only: export all customers as CSV."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/login/')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Phone', 'Email', 'City', 'Pincode', 'Referral Code', 'Joined'])
    for c in Customer.objects.order_by('-created_at'):
        writer.writerow([
            c.id, c.name, c.phone, c.email or '',
            c.city, c.pincode, c.referral_code or '',
            c.created_at.strftime('%d/%m/%Y'),
        ])
    return response


def export_appointments_csv(request):
    """Admin-only: export all appointments as CSV."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/login/')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="appointments.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Phone', 'Service', 'Date', 'Time', 'Confirmed', 'Notes', 'Booked On'])
    for a in Appointment.objects.order_by('-preferred_date'):
        writer.writerow([
            a.id, a.name, a.phone, a.get_service_type_display(),
            a.preferred_date, a.preferred_time,
            'Yes' if a.is_confirmed else 'No',
            a.notes, a.created_at.strftime('%d/%m/%Y'),
        ])
    return response