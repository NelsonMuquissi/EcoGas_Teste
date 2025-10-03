from django.urls import path
from . import views

urlpatterns = [
    # URLs ORIGINAIS (com problema)
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    
    # URLs TEMPORÁRIAS (funcionais)
    path('simple/', views.dashboard_simple, name='dashboard_simple'),
    path('simple-login/', views.login_view_simple, name='login_simple'),
    
    # Resto das URLs...
    path('logout/', views.logout_view, name='logout'),
    path('orders/', views.orders_view, name='orders'),
    path('users/', views.users_view, name='users'),
    path('deliveries/', views.deliveries_view, name='deliveries'),
    path('products/', views.products_view, name='products'),
    path('api/update-order-status/<str:order_id>/', views.update_order_status, name='update_order_status'),
    path('system-status/', views.system_status_view, name='system_status'),
]