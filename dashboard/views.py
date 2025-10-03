from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from api.advanced_hybrid_client import advanced_hybrid_api

def login_view(request):
    """Sistema de login 100% real com API"""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        print(f"🔐 Tentando autenticação real: {email}")
        
        # Autenticação real na API
        success, result = advanced_hybrid_api.login(email, password)
        
        if success:
            # Criar usuário local para sessão Django
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    'email': email,
                    'is_staff': True,
                    'is_active': True,
                    'first_name': result.get('user', {}).get('name', 'Admin')
                }
            )
            
            if created:
                user.set_unusable_password()  # Não usamos senha local
                user.save()
            
            # Login no Django
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            
            # Mensagem de sucesso
            messages.success(request, '🎉 Login realizado com sucesso!')
            messages.info(request, 'Conectado à API EcoGás em tempo real')
            
            return redirect('dashboard')
        else:
            # Mensagem de erro real da API
            error_msg = result.get('error', 'Credenciais inválidas')
            messages.error(request, f'❌ Falha na autenticação: {error_msg}')
    
    return render(request, 'dashboard/login.html')

def logout_view(request):
    """Logout do sistema"""
    logout(request)
    messages.info(request, 'Sessão encerrada com sucesso!')
    return redirect('login')

@login_required
def dashboard(request):
    """Dashboard principal com dados reais"""
    # Obter estatísticas reais
    success, stats_data = advanced_hybrid_api.get_admin_stats()
    
    # Obter pedidos recentes
    success_orders, orders_data = advanced_hybrid_api.get_all_orders()
    
    # Status do sistema
    system_status = advanced_hybrid_api.get_system_status()
    
    # CORREÇÃO: Lidar com diferentes formatos de resposta
    recent_orders = []
    if success_orders:
        if isinstance(orders_data, list):
            # Se a API retornar uma lista diretamente
            recent_orders = orders_data[:5]
        elif isinstance(orders_data, dict) and 'orders' in orders_data:
            # Se a API retornar um objeto com chave 'orders'
            recent_orders = orders_data.get('orders', [])[:5]
        else:
            # Formato inesperado
            recent_orders = []
    
    context = {
        'page_title': 'Dashboard EcoGás',
        'stats': stats_data if success else {},
        'recent_orders': recent_orders,
        'system_status': system_status,
        'active_tab': 'dashboard'
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def orders_view(request):
    """Gestão de pedidos reais"""
    success, orders_data = advanced_hybrid_api.get_all_orders()
    system_status = advanced_hybrid_api.get_system_status()
    
    # CORREÇÃO: Lidar com diferentes formatos de resposta
    orders = []
    if success:
        if isinstance(orders_data, list):
            orders = orders_data
        elif isinstance(orders_data, dict) and 'orders' in orders_data:
            orders = orders_data.get('orders', [])
        else:
            orders = []
    
    context = {
        'page_title': 'Gestão de Pedidos',
        'orders': orders,
        'system_status': system_status,
        'active_tab': 'orders'
    }
    return render(request, 'dashboard/orders.html', context)

@login_required
def users_view(request):
    """Gestão de usuários reais"""
    success, users_data = advanced_hybrid_api.get_all_users()
    system_status = advanced_hybrid_api.get_system_status()
    
    # CORREÇÃO: Lidar com diferentes formatos de resposta
    users = []
    if success:
        if isinstance(users_data, list):
            users = users_data
        elif isinstance(users_data, dict) and 'users' in users_data:
            users = users_data.get('users', [])
        else:
            users = []
    
    context = {
        'page_title': 'Gestão de Usuários',
        'users': users,
        'system_status': system_status,
        'active_tab': 'users'
    }
    return render(request, 'dashboard/users.html', context)

@login_required
def deliveries_view(request):
    """Entregas em tempo real"""
    success, deliveries_data = advanced_hybrid_api.get_live_deliveries()
    system_status = advanced_hybrid_api.get_system_status()
    
    # CORREÇÃO: Lidar com diferentes formatos de resposta
    deliveries = []
    if success:
        if isinstance(deliveries_data, list):
            deliveries = deliveries_data
        elif isinstance(deliveries_data, dict) and 'deliveries' in deliveries_data:
            deliveries = deliveries_data.get('deliveries', [])
        else:
            deliveries = []
    
    context = {
        'page_title': 'Entregas em Tempo Real',
        'deliveries': deliveries,
        'system_status': system_status,
        'active_tab': 'deliveries'
    }
    return render(request, 'dashboard/deliveries.html', context)

@login_required
def products_view(request):
    """Gestão de produtos reais"""
    success, products = advanced_hybrid_api.get_products()
    system_status = advanced_hybrid_api.get_system_status()
    
    # CORREÇÃO: Garantir que products seja uma lista
    if not success or not products:
        products = []
    
    context = {
        'page_title': 'Gestão de Produtos',
        'products': products if isinstance(products, list) else [],
        'system_status': system_status,
        'active_tab': 'products'
    }
    return render(request, 'dashboard/products.html', context)

@login_required
def update_order_status(request, order_id):
    """Atualiza status do pedido na API real"""
    if request.method == 'POST':
        new_status = request.POST.get('status')
        success, result = advanced_hybrid_api.update_order_status(order_id, new_status)
        
        if success:
            messages.success(request, f'✅ Pedido #{order_id} atualizado para: {new_status}')
        else:
            messages.error(request, f'❌ Erro ao atualizar pedido: {result.get("error")}')
    
    return redirect('orders')

@login_required
def system_status_view(request):
    """Página de status do sistema"""
    system_status = advanced_hybrid_api.get_system_status()
    
    context = {
        'page_title': 'Status do Sistema',
        'system_status': system_status,
        'active_tab': 'status'
    }
    return render(request, 'dashboard/system_status.html', context)