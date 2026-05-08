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
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    price_range = models.CharField(max_length=100, blank=True, help_text="e.g. ₹500 - ₹2000")
    image_url = models.URLField(blank=True, help_text="External image URL")
    is_featured = models.BooleanField(default=False)
    brand = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

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
# NEW MODELS
# ─────────────────────────────────────────────

class Customer(models.Model):
    """
    Simple custom customer model — no Django auth dependency.
    Phone is the primary identifier (common in India).
    Password stored as hashed string via make_password/check_password.
    """
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    password = models.CharField(max_length=255)  # store hashed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')

    # Product can be DB product or a free-text name (for DEFAULT_PRODUCTS fallback)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=200)  # always store name as string too
    product_price_range = models.CharField(max_length=100, blank=True)

    # Delivery details
    delivery_address = models.TextField()
    delivery_city = models.CharField(max_length=100)
    delivery_pincode = models.CharField(max_length=10)
    landmark = models.CharField(max_length=200, blank=True)

    # Order details
    notes = models.TextField(blank=True, help_text="Special requirements, prescription details, etc.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name} - {self.product_name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class Appointment(models.Model):
    SERVICE_CHOICES = [
        ('eye_checkup', 'Eye Checkup / आंख जांच'),
        ('frame_selection', 'Frame Selection Help'),
        ('contact_lens', 'Contact Lens Fitting'),
        ('repair', 'Frame Repair'),
        ('prescription', 'Power Check / Prescription'),
        ('other', 'Other'),
    ]

    # Customer can book as guest (phone) or as logged-in customer
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='eye_checkup')
    preferred_date = models.DateField()
    preferred_time = models.CharField(max_length=20)  # "10:00 AM", "2:00 PM" etc.
    notes = models.TextField(blank=True)

    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appt: {self.name} - {self.service_type} on {self.preferred_date}"

    class Meta:
        ordering = ['-preferred_date', 'preferred_time']
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"