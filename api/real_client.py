import requests
import json
from django.conf import settings

class RealEcoGasAPI:
    def __init__(self):
        self.base_url = "https://api-ecogas.onrender.com"
        self.token = None
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'EcoGas-Admin/1.0.0'
        })
    
    def _get_headers(self):
        headers = {}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def register(self, name, email, password, phone, role="CUSTOMER"):
        """Registra usuário seguindo o modelo User real"""
        try:
            url = f"{self.base_url}/auth/register"
            payload = {
                "name": name,
                "email": email,
                "password": password,
                "phone": phone,
                "role": role  # CUSTOMER, DELIVERY_PERSON, ADMIN
            }
            
            print(f"👤 Registrando: {email} como {role}")
            response = self.session.post(url, json=payload, timeout=15)
            print(f"📡 Status: {response.status_code}")
            
            if response.status_code == 201:
                data = response.json()
                print("✅ Registro bem-sucedido!")
                return True, data
            else:
                error_data = response.json()
                error_msg = error_data.get('error', error_data.get('message', response.text))
                print(f"❌ Erro: {error_msg}")
                return False, {'error': error_msg}
                
        except Exception as e:
            error = f'Erro no registro: {str(e)}'
            print(f"❌ {error}")
            return False, {'error': error}
    
    def login(self, email, password):
        """Login real com a API"""
        try:
            url = f"{self.base_url}/auth/login"
            payload = {"email": email, "password": password}
            
            print(f"🔐 Tentando login: {email}")
            response = self.session.post(url, json=payload, timeout=15)
            print(f"📡 Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                if self.token:
                    self.session.headers.update({'Authorization': f'Bearer {self.token}'})
                    print("✅ Login bem-sucedido!")
                    return True, data
                else:
                    return False, {'error': 'Token não recebido'}
            else:
                # Tenta extrair mensagem de erro
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', error_data.get('message', response.text))
                except:
                    error_msg = response.text
                
                print(f"❌ Login falhou: {error_msg}")
                return False, {'error': error_msg}
                
        except Exception as e:
            error = f'Erro no login: {str(e)}'
            print(f"❌ {error}")
            return False, {'error': error}
    
    def _make_request(self, method, endpoint, data=None):
        """Método genérico para requests"""
        try:
            url = f"{self.base_url}{endpoint}"
            print(f"🌐 {method} {url}")
            
            headers = self._get_headers()
            response = self.session.request(method, url, json=data, headers=headers, timeout=10)
            print(f"📡 Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                return True, response.json()
            elif response.status_code == 401:
                return False, {'error': 'Não autorizado - Faça login novamente'}
            elif response.status_code == 403:
                return False, {'error': 'Acesso negado - Permissões insuficientes'}
            elif response.status_code == 404:
                return False, {'error': 'Endpoint não encontrado'}
            else:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', error_data.get('message', response.text))
                except:
                    error_msg = response.text
                return False, {'error': error_msg}
                
        except Exception as e:
            return False, {'error': f'Erro de conexão: {str(e)}'}
    
    # Métodos baseados nos modelos reais
    
    # User endpoints
    def get_all_users(self):
        """GET /admin/users - Retorna todos os usuários"""
        return self._make_request('GET', '/admin/users')
    
    def update_user_role(self, user_id, new_role):
        """PATCH /admin/users/{id}/role - Altera role do usuário"""
        return self._make_request('PATCH', f'/admin/users/{user_id}/role', {'role': new_role})
    
    # Product endpoints
    def get_products(self):
        """GET /products - Lista produtos (público)"""
        return self._make_request('GET', '/products')
    
    def create_product(self, product_data):
        """POST /admin/products - Cria novo produto (admin apenas)"""
        return self._make_request('POST', '/admin/products', product_data)
    
    # Order endpoints
    def get_all_orders(self):
        """GET /admin/orders - Todos os pedidos (admin)"""
        return self._make_request('GET', '/admin/orders')
    
    def get_user_orders(self):
        """GET /orders - Pedidos do usuário logado"""
        return self._make_request('GET', '/orders')
    
    def create_order(self, order_data):
        """POST /orders - Cria novo pedido"""
        return self._make_request('POST', '/orders', order_data)
    
    def update_order_status(self, order_id, new_status):
        """PATCH /orders/{id}/status - Atualiza status do pedido"""
        return self._make_request('PATCH', f'/orders/{order_id}/status', {'status': new_status})
    
    # Delivery endpoints
    def get_live_deliveries(self):
        """GET /admin/deliveries/live - Entregas em tempo real"""
        return self._make_request('GET', '/admin/deliveries/live')
    
    def get_delivery_orders(self):
        """GET /delivery/orders - Pedidos para entregadores"""
        return self._make_request('GET', '/delivery/orders')
    
    def accept_delivery_order(self, order_id):
        """PATCH /delivery/orders/{id}/accept - Aceita pedido para entrega"""
        return self._make_request('PATCH', f'/delivery/orders/{order_id}/accept')
    
    def update_delivery_location(self, order_id, location_data):
        """POST /delivery/orders/{order_id}/location - Atualiza localização"""
        return self._make_request('POST', f'/delivery/orders/{order_id}/location', location_data)
    
    # Address endpoints
    def get_user_addresses(self):
        """GET /addresses - Endereços do usuário"""
        return self._make_request('GET', '/addresses')
    
    def create_address(self, address_data):
        """POST /addresses - Cria novo endereço"""
        return self._make_request('POST', '/addresses', address_data)
    
    # Admin endpoints
    def get_admin_stats(self):
        """GET /admin/stats - Estatísticas do admin"""
        return self._make_request('GET', '/admin/stats')
    
    def get_dashboard(self):
        """GET /dashboard - Dashboard do usuário"""
        return self._make_request('GET', '/dashboard')

# Instância global
real_api = RealEcoGasAPI()