from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from api.robust_hybrid_client import robust_hybrid_api
import logging

logger = logging.getLogger(__name__)

def login_view(request):
    """Sistema de login robusto com tratamento de erros"""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        try:
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')
            
            if not email:
                messages.error(request, 'Email é obrigatório.')
                return render(request, 'dashboard/login.html')
            
            # Usa o cliente robusto (100% mock por enquanto)
            success, result = robust_hybrid_api.login(email, password)
            
            if success:
                try:
                    # Tenta buscar usuário existente primeiro
                    try:
                        user = User.objects.get(username=email)
                        # Atualiza dados do usuário existente
                        user.first_name = result['user']['name']
                        user.email = email
                        user.save()
                    except User.DoesNotExist:
                        # Cria novo usuário
                        user = User.objects.create_user(
                            username=email,
                            email=email,
                            first_name=result['user']['name'],
                            is_staff=True,
                            is_active=True
                        )
                        user.set_unusable_password()
                        user.save()
                    
                    # Login do usuário
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    
                    # Mensagens informativas
                    messages.info(request, '��� Modo Demonstração')
                    messages.success(request, f'Bem-vindo, {result["user"]["name"]}!')
                    messages.warning(request, '��� API em manutenção - Dados de exemplo')
                    
                    return redirect('dashboard')
                    
                except Exception as e:
                    logger.error(f"Erro ao criar/atualizar usuário: {e}")
                    messages.error(request, 'Erro interno do sistema. Tente novamente.')
                    return render(request, 'dashboard/login.html')
            else:
                messages.error(request, 'Falha na autenticação.')
                
        except Exception as e:
            logger.error(f"Erro no login: {e}")
            messages.error(request, 'Erro interno do sistema. Tente novamente.')
    
    return render(request, 'dashboard/login.html')

def logout_view(request):
    """Logout do sistema"""
    logout(request)
    messages.info(request, 'Sessão encerrada com sucesso!')
    return redirect('login')

@login_required
def dashboard(request):
    """Dashboard principal"""
    try:
        success, stats = robust_hybrid_api.get_admin_stats()
        
        # Adiciona pedidos recentes
        success_orders, orders_data = robust_hybrid_api.get_all_orders()
        if success_orders:
            stats['recent_orders'] = orders_data.get('orders', [])[:5]
        
        # Status do sistema
        system_status = robust_hybrid_api.get_system_status()
        
        context = {
            'page_title': 'Dashboard EcoGás',
            'stats': stats if success else {},
            'system_status': system_status,
            'active_tab': 'dashboard'
        }
        return render(request, 'dashboard/dashboard.html', context)
    except Exception as e:
        logger.error(f"Erro no dashboard: {e}")
        messages.error(request, 'Erro ao carregar dashboard.')
        return render(request, 'dashboard/dashboard.html', {'stats': {}, 'system_status': {}})

@login_required
def orders_view(request):
    """Gestão de pedidos"""
    try:
        success, orders_data = robust_hybrid_api.get_all_orders()
        system_status = robust_hybrid_api.get_system_status()
        
        context = {
            'page_title': 'Gestão de Pedidos',
            'orders': orders_data.get('orders', []) if success else [],
            'system_status': system_status,
            'active_tab': 'orders'
        }
        return render(request, 'dashboard/orders.html', context)
    except Exception as e:
        logger.error(f"Erro na página de pedidos: {e}")
        messages.error(request, 'Erro ao carregar pedidos.')
        return render(request, 'dashboard/orders.html', {'orders': [], 'system_status': {}})

@login_required
def users_view(request):
    """Gestão de usuários"""
    try:
        success, users_data = robust_hybrid_api.get_all_users()
        system_status = robust_hybrid_api.get_system_status()
        
        context = {
            'page_title': 'Gestão de Usuários', 
            'users': users_data.get('users', []) if success else [],
            'system_status': system_status,
            'active_tab': 'users'
        }
        return render(request, 'dashboard/users.html', context)
    except Exception as e:
        logger.error(f"Erro na página de usuários: {e}")
        messages.error(request, 'Erro ao carregar usuários.')
        return render(request, 'dashboard/users.html', {'users': [], 'system_status': {}})

@login_required
def deliveries_view(request):
    """Acompanhamento de entregas"""
    try:
        success, deliveries_data = robust_hybrid_api.get_live_deliveries()
        system_status = robust_hybrid_api.get_system_status()
        
        context = {
            'page_title': 'Entregas em Tempo Real',
            'deliveries': deliveries_data.get('deliveries', []) if success else [],
            'system_status': system_status,
            'active_tab': 'deliveries'
        }
        return render(request, 'dashboard/deliveries.html', context)
    except Exception as e:
        logger.error(f"Erro na página de entregas: {e}")
        messages.error(request, 'Erro ao carregar entregas.')
        return render(request, 'dashboard/deliveries.html', {'deliveries': [], 'system_status': {}})

@login_required
def products_view(request):
    """Gestão de produtos"""
    try:
        success, products = robust_hybrid_api.get_products()
        system_status = robust_hybrid_api.get_system_status()
        
        context = {
            'page_title': 'Gestão de Produtos',
            'products': products if success else [],
            'system_status': system_status,
            'active_tab': 'products'
        }
        return render(request, 'dashboard/products.html', context)
    except Exception as e:
        logger.error(f"Erro na página de produtos: {e}")
        messages.error(request, 'Erro ao carregar produtos.')
        return render(request, 'dashboard/products.html', {'products': [], 'system_status': {}})

@login_required
def update_order_status(request, order_id):
    """API endpoint para atualizar status do pedido"""
    if request.method == 'POST':
        try:
            new_status = request.POST.get('status')
            success, result = robust_hybrid_api.update_order_status(order_id, new_status)
            
            if success:
                messages.success(request, f'✅ Pedido #{order_id} atualizado para: {new_status}')
            else:
                messages.error(request, f'❌ Erro ao atualizar pedido: {result.get("error")}')
        except Exception as e:
            logger.error(f"Erro ao atualizar pedido: {e}")
            messages.error(request, 'Erro ao atualizar pedido.')
    
    return redirect('orders')
