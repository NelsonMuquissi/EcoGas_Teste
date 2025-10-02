from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from api.advanced_hybrid_client import advanced_hybrid_api  # 🔄 Novo cliente

def login_view(request):
    """Sistema de login inteligente"""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Usa o cliente hybrid API avançado
        success, result = advanced_hybrid_api.login(email, password)
        
        if success:
            # Cria ou busca usuário local
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    'email': email, 
                    'is_staff': True,
                    'is_active': True,
                    'first_name': result['user']['name']
                }
            )
            
            if created:
                user.set_unusable_password()
                user.save()
            
            # Especifica o backend manualmente
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            
            login(request, user)
            
            # Mensagem informativa sobre o status
            system_status = advanced_hybrid_api.get_system_status()
            if system_status['using_real_api']:
                messages.success(request, '🎉 Conectado à API real!')
                messages.info(request, 'Sistema operando com dados em tempo real')
            else:
                messages.warning(request, '⚠️  Modo de demonstração')
                messages.info(request, 'Usando dados de exemplo - API em manutenção')
                
            return redirect('dashboard')
        else:
            messages.error(request, 'Falha na autenticação.')
    
    return render(request, 'dashboard/login.html')

def logout_view(request):
    """Logout do sistema"""
    logout(request)
    messages.info(request, 'Sessão encerrada com sucesso!')
    return redirect('login')

@login_required
def dashboard(request):
    """Dashboard principal com status do sistema"""
    success, stats = advanced_hybrid_api.get_admin_stats()
    
    # Adiciona pedidos recentes
    success_orders, orders_data = advanced_hybrid_api.get_all_orders()
    if success_orders:
        stats['recent_orders'] = orders_data.get('orders', [])[:5]
    
    # Status do sistema
    system_status = advanced_hybrid_api.get_system_status()
    
    context = {
        'page_title': 'Dashboard EcoGás',
        'stats': stats if success else {},
        'system_status': system_status,
        'active_tab': 'dashboard'
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def orders_view(request):
    """Gestão de pedidos"""
    success, orders_data = advanced_hybrid_api.get_all_orders()
    system_status = advanced_hybrid_api.get_system_status()
    
    context = {
        'page_title': 'Gestão de Pedidos',
        'orders': orders_data.get('orders', []) if success else [],
        'system_status': system_status,
        'active_tab': 'orders'
    }
    return render(request, 'dashboard/orders.html', context)

@login_required
def users_view(request):
    """Gestão de usuários"""
    success, users_data = advanced_hybrid_api.get_all_users()
    system_status = advanced_hybrid_api.get_system_status()
    
    context = {
        'page_title': 'Gestão de Usuários', 
        'users': users_data.get('users', []) if success else [],
        'system_status': system_status,
        'active_tab': 'users'
    }
    return render(request, 'dashboard/users.html', context)

@login_required
def deliveries_view(request):
    """Acompanhamento de entregas"""
    success, deliveries_data = advanced_hybrid_api.get_live_deliveries()
    system_status = advanced_hybrid_api.get_system_status()
    
    context = {
        'page_title': 'Entregas em Tempo Real',
        'deliveries': deliveries_data.get('deliveries', []) if success else [],
        'system_status': system_status,
        'active_tab': 'deliveries'
    }
    return render(request, 'dashboard/deliveries.html', context)

@login_required
def products_view(request):
    """Gestão de produtos"""
    success, products = advanced_hybrid_api.get_products()
    system_status = advanced_hybrid_api.get_system_status()
    
    context = {
        'page_title': 'Gestão de Produtos',
        'products': products if success else [],
        'system_status': system_status,
        'active_tab': 'products'
    }
    return render(request, 'dashboard/products.html', context)

@login_required
def update_order_status(request, order_id):
    """API endpoint para atualizar status do pedido"""
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