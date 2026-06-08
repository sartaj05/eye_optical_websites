# Eye Drishti Optical – New Features Guide

## 🆕 New Features Added

### 1. 📋 Prescription / Eye Power Storage
Customers can view their eye prescriptions from their dashboard.
Admin saves the prescription via the admin dashboard after an eye checkup.
- **URL:** `/prescription/<id>/`  
- **Template:** `prescription.html` (printable — includes a Print/PDF button)
- **Admin:** Go to Admin Dashboard → Add Prescription for a customer
- **Customer sees:** SPH, CYL, Axis, ADD, VA for both eyes + PD + doctor notes

---

### 2. ❤️ Wishlist
Customers can save products to their wishlist.
- Works via **AJAX** (no page reload) — just a POST to `/wishlist/toggle/`
- To add a ❤️ button to a product card, add this to your product cards:
```html
<button onclick="toggleWishlist('{{ product.id }}', '{{ product.name }}')"
        class="wishlist-btn {% if product.id|stringformat:'s' in wishlist_ids %}active{% endif %}">
  ❤️
</button>
<script>
function toggleWishlist(id, name) {
  fetch('/wishlist/toggle/', {
    method: 'POST',
    headers: {'X-CSRFToken': '{{ csrf_token }}', 'Content-Type': 'application/x-www-form-urlencoded'},
    body: `product_id=${id}&product_name=${encodeURIComponent(name)}`
  }).then(r => r.json()).then(d => alert(d.message));
}
</script>
```
- Customer's saved products appear in their **Dashboard → Wishlist tab**

---

### 3. ⭐ Product Reviews
Customers can write reviews for DB products after purchase.
- **URL:** `/review/<product_id>/`
- Admin must **approve** reviews before they show publicly
- In Admin Dashboard → Reviews tab → Approve or Delete
- To show average rating on a product: `{{ product.avg_rating }}` (model property)
- To show review count: `{{ product.review_count }}`

---

### 4. 👤 Update Profile Page
Customers can update their name, email, address, city, pincode, and password.
- **URL:** `/profile/update/`
- **Template:** `update_profile.html`
- Phone cannot be changed (it's the primary identifier)
- Password change is optional — leave blank to keep old password

---

### 5. 🔗 Referral Program
Every customer gets a unique referral code (e.g., `RAH9045321`).
- Shareable link: `https://yoursite.com/login/?ref=YOURCODE`
- When someone registers with a referral code, they are linked as `referred_by`
- Customer can see their referral code and link in **Dashboard → Referrals tab**
- **Note:** The discount logic is not automated yet — you handle it manually.
  When you see a `referred_by` in the Customer list, give them a discount manually.

---

### 6. 🔬 Lens Customiser on Order Page
When placing an order (`/buy/<product_id>/`), customers can now choose:
- **Lens Type:** Single Vision, Bifocal, Progressive, Blue Cut, Photochromic
- **Lens Coating:** AR, UV400, Scratch Resistant, Photochromic, Mirror, None
- **Frame Color:** Black, Silver, Gold, Brown, Blue, Red, Transparent, Gunmetal

These selections are saved with the order and visible in Admin Dashboard.

---

### 7. 📦 New Order Status: "Shipped"
The `Order` model now has a `shipped` status between `confirmed` and `delivered`.

---

### 8. 📝 Admin Notes on Orders & Appointments
- Admin can add internal notes to orders and appointments from the dashboard.
- Notes are never shown to customers.

---

### 9. 📊 CSV Exports (Admin Only)
Three export buttons in Admin Dashboard:
| URL | File |
|-----|------|
| `/export/orders/` | `orders.csv` |
| `/export/customers/` | `customers.csv` |
| `/export/appointments/` | `appointments.csv` |

Add these links to your `admin_dashboard.html`:
```html
<a href="{% url 'export_orders_csv' %}">⬇️ Export Orders CSV</a>
<a href="{% url 'export_customers_csv' %}">⬇️ Export Customers CSV</a>
<a href="{% url 'export_appointments_csv' %}">⬇️ Export Appointments CSV</a>
```

---

## 🗂️ Files to Replace / Add

| File | Action |
|------|--------|
| `optical/models.py` | **REPLACE** with new `models.py` |
| `optical/views.py` | **REPLACE** with new `views.py` |
| `optical/urls.py` | **REPLACE** with new `urls.py` |
| `optical/templates/optical/prescription.html` | **ADD** new template |
| `optical/templates/optical/submit_review.html` | **ADD** new template |
| `optical/templates/optical/update_profile.html` | **ADD** new template |

---

## ⚙️ After Replacing Files

```bash
python manage.py makemigrations optical
python manage.py migrate
python manage.py runserver
```

Or just double-click `run_migrations.py`!

---

## 💡 More Feature Ideas (Future)

| Feature | Difficulty |
|---------|-----------|
| SMS confirmation via Twilio/MSG91 | Medium |
| WhatsApp auto-message on order | Easy (WhatsApp Business API) |
| Online payment via Razorpay | Medium |
| Lens power calculator widget | Easy |
| Virtual try-on (AR glasses) | Hard |
| Loyalty points system | Medium |
| Instagram feed embed on homepage | Easy |
| Google review widget | Easy |
| Product comparison tool | Medium |
| Stock management / low stock alert | Easy |