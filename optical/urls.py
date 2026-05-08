from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # Auth
    path('login/', views.customer_login, name='customer_login'),
    path('logout/', views.customer_logout, name='customer_logout'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),

    # Orders
    path('buy/<product_id>/', views.buy_product, name='buy_product'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),

    # Appointments
    path('appointment/', views.book_appointment, name='book_appointment'),
    path('appointment/success/<int:appt_id>/', views.appointment_success, name='appointment_success'),
]