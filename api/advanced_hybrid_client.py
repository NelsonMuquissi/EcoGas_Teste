import requests
import time
from datetime import datetime
from django.conf import settings

class EcoGasRealAPI:
    def __init__(self):
        self.base_url = settings.ECO_GAS_API_URL
        self.token = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'EcoGas-Admin/1.0.0',
            'Content-Type': 'application/json'
        })
    
    def _make_request(self, endpoint, method='GET', data=None, max_retries=2):
        """Faz request para a API com sistema de retry"""
        for attempt in range(max_retries + 1):
            try:
                url = f"{self.base_url}{endpoint}"
                headers = {}
                
                if self.token:
                    headers['Authorization'] = f'Bearer {self.token}'
                
                print(f"🌐 Request {attempt+1}/{max_retries+1}: {method} {url}")
                
                if method.upper() == 'GET':
                    response = self.session.get(url, headers=headers, timeout=10)
                else:
                    response = self.session.request(method, url, json=data, headers=headers, timeout=10)
                
                print(f"📡 Response: {response.status_code}")
                print(f"📦 Response data type: {type(response.json())}")
                print(f"📦 Response data: {response.json()}")
                
                if response.status_code == 200:
                    return True, response.json()
                elif response.status_code == 401:
                    return False, {"error": "Não autorizado - Faça login novamente"}
                elif response.status_code == 403:
                    return False, {"error": "Acesso negado - Permissões insuficientes"}
                elif response.status_code == 404:
                    return False, {"error": "Endpoint não encontrado"}
                else:
                    error_msg = response.json().get('error', f'HTTP {response.status_code}')
                    return False, {"error": error_msg}
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries:
                    print(f"⏳ Timeout, tentando novamente... ({attempt + 1}/{max_retries})")
                    time.sleep(1)
                else:
                    return False, {"error": "Timeout - API não respondeu"}
            except requests.exceptions.ConnectionError:
                if attempt < max_retries:
                    print(f"🔌 Erro de conexão, tentando novamente... ({attempt + 1}/{max_retries})")
                    time.sleep(1)
                else:
                    return False, {"error": "Erro de conexão - Verifique a URL da API"}
            except Exception as e:
                return False, {"error": f"Erro inesperado: {str(e)}"}
    
    def login(self, email, password):
        """Autentica na API real"""
        print(f"🔐 Tentando login real para: {email}")
        
        success, result = self._make_request(
            "/auth/login", 
            method='POST',
            data={
                "login": email,  # Campo correto conforme documentação
                "password": password
            }
        )
        
        if success:
            self.token = result.get('token')
            print("✅ Login REAL bem-sucedido!")
            return True, result
        else:
            print(f"❌ Falha no login: {result.get('error')}")
            return False, result
    
    def get_admin_stats(self):
        """Obtém estatísticas administrativas da API real"""
        return self._make_request("/admin/stats")
    
    def get_all_orders(self):
        """Obtém todos os pedidos da API real"""
        return self._make_request("/admin/orders")
    
    def get_all_users(self):
        """Obtém todos os usuários da API real"""
        return self._make_request("/admin/users")
    
    def get_products(self):
        """Obtém produtos da API real (endpoint público)"""
        return self._make_request("/products")
    
    def get_live_deliveries(self):
        """Obtém entregas em tempo real da API real"""
        return self._make_request("/admin/deliveries/live")
    
    def update_order_status(self, order_id, new_status):
        """Atualiza status do pedido na API real"""
        return self._make_request(
            f"/orders/{order_id}/status",
            method='PATCH',
            data={"status": new_status}
        )
    
    def get_system_status(self):
        """Verifica status da API"""
        success, _ = self._make_request("/products", max_retries=0)
        return {
            "api_status": "online" if success else "offline",
            "base_url": self.base_url,
            "authenticated": bool(self.token)
        }

# Instância global
advanced_hybrid_api = EcoGasRealAPI()