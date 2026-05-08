# Eye Drishti Optical – Django Project Setup Guide

## ⚡ FIX THE ERROR FIRST (Run these commands!)

The error `no such table: optical_inquiry` means migrations were never run.
Open your terminal in the project folder and run:

```bash
cd C:\Users\91830\Desktop\eye_project\eye_drishti_optical
python manage.py makemigrations optical
python manage.py migrate
python manage.py runserver
```

That's it! The error will be gone.

---

## 📁 Complete File Structure

```
eye_project/
└── eye_drishti_optical/
    ├── eye_drishti/
    │   ├── settings.py
    │   ├── urls.py          ← Add optical.urls here
    │   └── wsgi.py
    ├── optical/
    │   ├── migrations/      ← Auto-created after makemigrations
    │   ├── templates/
    │   │   └── optical/
    │   │       └── home.html   ← PASTE home.html here
    │   ├── __init__.py
    │   ├── admin.py         ← REPLACE with provided admin.py
    │   ├── apps.py
    │   ├── models.py        ← REPLACE with provided models.py
    │   ├── urls.py          ← REPLACE with provided urls.py
    │   └── views.py         ← REPLACE with provided views.py
    └── manage.py
```

---

## 🔧 Step-by-Step Setup

### 1. Replace/Update Files

Copy the provided files into your `optical/` app folder:
- `models.py` → `optical/models.py`
- `views.py`  → `optical/views.py`
- `admin.py`  → `optical/admin.py`
- `urls.py`   → `optical/urls.py`

### 2. Create Template Folder

```bash
mkdir -p optical/templates/optical
```

Copy `home.html` → `optical/templates/optical/home.html`

### 3. Update eye_drishti/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('optical.urls')),
]
```

### 4. Run Migrations

```bash
python manage.py makemigrations optical
python manage.py migrate
```

### 5. Create Superuser (for Admin Panel)

```bash
python manage.py createsuperuser
```

### 6. Run Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## 🎛️ Admin Panel Features

Visit http://127.0.0.1:8000/admin to:
- **View all customer inquiries** (from contact form)
- **Add/Edit Products** – Add your own frames with real photos
- **Add Testimonials** – Add real customer reviews
- **Manage everything** from a nice dashboard

---

## 🌟 Website Features

✅ Real shop images from Google Maps (provided URLs)
✅ Product filter by category (Eyeglasses, Sunglasses, etc.)
✅ Floating WhatsApp + Call buttons
✅ Contact form → saves to database (optical_inquiry table)
✅ FAQ accordion
✅ Google Maps embed
✅ Mobile responsive
✅ Announcement scrolling bar
✅ Sticky navbar with active section highlight
✅ 4.7★ rating display with bar chart
✅ Customer testimonials section
✅ SEO meta tags (Hindi + English keywords)
✅ Click-to-call + WhatsApp integration
✅ Admin panel to manage everything

---

## 🛒 Add Real Products via Admin

1. Go to http://127.0.0.1:8000/admin
2. Click "Products" → "Add Product"
3. Fill in: Name, Category, Price, Image URL, Brand
4. Check "Is Featured" to show on homepage

---

## 📞 Shop Details (Pre-configured)

- **Name**: Eye Drishti Optical
- **Phone**: +91 90447 90354
- **Address**: Shop No. 6, Nayab Market, Kachahri Road, Near SBI Bank, Pratapgarh UP 230001
- **Hours**: Mon–Sat 10 AM – 8 PM
- **WhatsApp**: 919044790354

To change any detail, edit the `BUSINESS_INFO` dict in `views.py`.