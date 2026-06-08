from django.db import models


class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer Inquiry"
        verbose_name_plural = "Customer Inquiries"


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('eyeglasses', 'Eyeglasses'),
        ('sunglasses', 'Sunglasses'),
        ('contact_lenses', 'Contact Lenses'),
        ('frames', 'Frames'),
        ('reading_glasses', 'Reading Glasses'),
        ('accessories', 'Accessories'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    price_range = models.CharField(max_length=100, blank=True, help_text="e.g. ₹500 - ₹2000")
    image_url = models.URLField(blank=True, help_text="External image URL")
    is_featured = models.BooleanField(default=False)
    brand = models.CharField(max_length=100, blank=True)
    stock_available = models.BooleanField(default=True)  # NEW: in stock flag
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def avg_rating(self):
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None

    @property
    def review_count(self):
        return self.reviews.filter(is_approved=True).count()

    class Meta:
        ordering = ['-is_featured', 'name']


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    rating = models.IntegerField(default=5)
    review = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.rating}★"

    class Meta:
        ordering = ['-created_at']


# ─────────────────────────────────────────────
# CUSTOMER MODEL
# ─────────────────────────────────────────────

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    password = models.CharField(max_length=255)
    # NEW: referral code
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='referrals'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

    def save(self, *args, **kwargs):
        # Auto-generate a unique referral code on first save
        if not self.referral_code:
            import random, string
            base = (self.name[:3] + self.phone[-3:]).upper()
            suffix = ''.join(random.choices(string.digits, k=3))
            self.referral_code = base + suffix
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


# ─────────────────────────────────────────────
# ORDER MODEL
# ─────────────────────────────────────────────

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),      # NEW
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=200)
    product_price_range = models.CharField(max_length=100, blank=True)

    # Delivery details
    delivery_address = models.TextField()
    delivery_city = models.CharField(max_length=100)
    delivery_pincode = models.CharField(max_length=10)
    landmark = models.CharField(max_length=200, blank=True)

    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # NEW: Lens customisation fields
    lens_type = models.CharField(max_length=100, blank=True,
        help_text="e.g. Single Vision, Bifocal, Progressive, Blue Cut")
    lens_coating = models.CharField(max_length=100, blank=True,
        help_text="e.g. Anti-Reflection, Photochromic, UV400")
    frame_color = models.CharField(max_length=50, blank=True)

    # NEW: admin tracking note
    admin_note = models.TextField(blank=True, help_text="Internal note for staff only")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name} - {self.product_name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order"
        verbose_name_plural = "Orders"


# ─────────────────────────────────────────────
# APPOINTMENT MODEL
# ─────────────────────────────────────────────

class Appointment(models.Model):
    SERVICE_CHOICES = [
        ('eye_checkup', 'Eye Checkup / आंख जांच'),
        ('frame_selection', 'Frame Selection Help'),
        ('contact_lens', 'Contact Lens Fitting'),
        ('repair', 'Frame Repair'),
        ('prescription', 'Power Check / Prescription'),
        ('other', 'Other'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='eye_checkup')
    preferred_date = models.DateField()
    preferred_time = models.CharField(max_length=20)
    notes = models.TextField(blank=True)

    is_confirmed = models.BooleanField(default=False)
    # NEW: admin internal note
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appt: {self.name} - {self.service_type} on {self.preferred_date}"

    class Meta:
        ordering = ['-preferred_date', 'preferred_time']
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"


# ─────────────────────────────────────────────
# NEW: PRESCRIPTION / EYE POWER RECORD
# ─────────────────────────────────────────────

class Prescription(models.Model):
    """
    Stores a customer's eye prescription / power record.
    Customers can view their own prescriptions from the dashboard.
    Only admin can create/edit these.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='prescriptions')

    # Exam date
    exam_date = models.DateField()

    # Right Eye (OD)
    right_sph = models.CharField(max_length=10, blank=True, verbose_name="Right SPH")
    right_cyl = models.CharField(max_length=10, blank=True, verbose_name="Right CYL")
    right_axis = models.CharField(max_length=10, blank=True, verbose_name="Right Axis")
    right_add = models.CharField(max_length=10, blank=True, verbose_name="Right ADD (near)")
    right_va = models.CharField(max_length=10, blank=True, verbose_name="Right VA")

    # Left Eye (OS)
    left_sph = models.CharField(max_length=10, blank=True, verbose_name="Left SPH")
    left_cyl = models.CharField(max_length=10, blank=True, verbose_name="Left CYL")
    left_axis = models.CharField(max_length=10, blank=True, verbose_name="Left Axis")
    left_add = models.CharField(max_length=10, blank=True, verbose_name="Left ADD (near)")
    left_va = models.CharField(max_length=10, blank=True, verbose_name="Left VA")

    # PD
    pd = models.CharField(max_length=20, blank=True, verbose_name="PD (Pupillary Distance)")

    # Notes
    notes = models.TextField(blank=True, verbose_name="Doctor Notes")

    # Link to appointment if created from one
    appointment = models.ForeignKey(
        Appointment, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='prescriptions'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rx for {self.customer.name} on {self.exam_date}"

    class Meta:
        ordering = ['-exam_date']
        verbose_name = "Prescription"
        verbose_name_plural = "Prescriptions"


# ─────────────────────────────────────────────
# NEW: PRODUCT REVIEW
# ─────────────────────────────────────────────

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=5, choices=[(i, f"{i}★") for i in range(1, 6)])
    review = models.TextField()
    is_approved = models.BooleanField(default=False, help_text="Admin must approve before showing")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} → {self.product.name} ({self.rating}★)"

    class Meta:
        ordering = ['-created_at']
        # One review per customer per product
        unique_together = ('product', 'customer')
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"


# ─────────────────────────────────────────────
# NEW: WISHLIST
# ─────────────────────────────────────────────

class WishlistItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishlist')
    # Store either DB product id or DEFAULT_PRODUCTS id string
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    product_name = models.CharField(max_length=200)   # always cache name
    product_id_str = models.CharField(max_length=20)  # 'dp_1' or '5' (db pk)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} ♥ {self.product_name}"

    class Meta:
        ordering = ['-added_at']
        unique_together = ('customer', 'product_id_str')
        verbose_name = "Wishlist Item"
        verbose_name_plural = "Wishlist Items"