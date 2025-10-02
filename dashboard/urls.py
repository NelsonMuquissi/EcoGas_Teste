from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('orders/', views.orders_view, name='orders'),
    path('users/', views.users_view, name='users'),
    path('deliveries/', views.deliveries_view, name='deliveries'),
    path('products/', views.products_view, name='products'),
    path('api/update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('system-status/', views.system_status_view, name='system_status'),
]