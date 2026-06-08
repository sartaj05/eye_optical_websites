from django.urls import path
from . import views

urlpatterns = [
    # ── Public ──────────────────────────────────────────────────────────────
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),

    # ── Auth ─────────────────────────────────────────────────────────────────
    path('login/', views.customer_login, name='customer_login'),
    path('logout/', views.customer_logout, name='customer_logout'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('profile/update/', views.update_profile, name='update_profile'),  # NEW

    # ── Orders ───────────────────────────────────────────────────────────────
    path('buy/<product_id>/', views.buy_product, name='buy_product'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),

    # ── Appointments ─────────────────────────────────────────────────────────
    path('appointment/', views.book_appointment, name='book_appointment'),
    path('appointment/success/<int:appt_id>/', views.appointment_success, name='appointment_success'),

    # ── Prescription ─────────────────────────────────────────────────────────
    path('prescription/<int:rx_id>/', views.view_prescription, name='view_prescription'),  # NEW

    # ── Wishlist ─────────────────────────────────────────────────────────────
    path('wishlist/toggle/', views.toggle_wishlist, name='toggle_wishlist'),  # NEW (AJAX POST)

    # ── Reviews ──────────────────────────────────────────────────────────────
    path('review/<int:product_id>/', views.submit_review, name='submit_review'),  # NEW

    # ── Admin Dashboard ──────────────────────────────────────────────────────
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # ── CSV Exports (admin only) ─────────────────────────────────────────────
    path('export/orders/', views.export_orders_csv, name='export_orders_csv'),         # NEW
    path('export/customers/', views.export_customers_csv, name='export_customers_csv'), # NEW
    path('export/appointments/', views.export_appointments_csv, name='export_appointments_csv'),  # NEW
]