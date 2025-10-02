from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from api.robust_hybrid_client import robust_hybrid_api

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        success, result = robust_hybrid_api.login(email, password)
        
        if success:
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    'email': email,
                    'first_name': result['user']['name'],
                    'is_staff': True,
                    'is_active': True
                }
            )
            if created:
                user.set_unusable_password()
                user.save()
            
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, f'Bem-vindo, {result["user"]["name"]}!')
            return redirect('dashboard')
    
    return render(request, 'dashboard/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Logout realizado!')
    return redirect('login')

@login_required
def dashboard(request):
    success, stats = robust_hybrid_api.get_admin_stats()
    context = {
        'page_title': 'Dashboard EcoGas',
        'stats': stats if success else {},
        'active_tab': 'dashboard'
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def orders_view(request):
    success, orders_data = robust_hybrid_api.get_all_orders()
    context = {
        'page_title': 'Gestao de Pedidos',
        'orders': orders_data.get('orders', []) if success else [],
        'active_tab': 'orders'
    }
    return render(request, 'dashboard/orders.html', context)

@login_required
def users_view(request):
    success, users_data = robust_hybrid_api.get_all_users()
    context = {
        'page_title': 'Gestao de Usuarios',
        'users': users_data.get('users', []) if success else [],
        'active_tab': 'users'
    }
    return render(request, 'dashboard/users.html', context)

@login_required
def deliveries_view(request):
    success, deliveries_data = robust_hybrid_api.get_live_deliveries()
    context = {
        'page_title': 'Entregas em Tempo Real',
        'deliveries': deliveries_data.get('deliveries', []) if success else [],
        'active_tab': 'deliveries'
    }
    return render(request, 'dashboard/deliveries.html', context)

@login_required
def products_view(request):
    success, products = robust_hybrid_api.get_products()
    context = {
        'page_title': 'Gestao de Produtos',
        'products': products if success else [],
        'active_tab': 'products'
    }
    return render(request, 'dashboard/products.html', context)

@login_required
def update_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        success, result = robust_hybrid_api.update_order_status(order_id, new_status)
        if success:
            messages.success(request, f'Pedido {order_id} atualizado!')
    return redirect('orders')
