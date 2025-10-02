import requests
from django.conf import settings
import json
import time

class EcoGasAPI:
    def __init__(self):
        self.base_url = "https://api-ecogas.onrender.com"
        self.token = None
        self.session = requests.Session()
        # Configurações para evitar timeout
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'EcoGas-Admin/1.0.0'
        })
    
    def _get_headers(self):
        headers = {}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def login(self, email, password):
        """Autentica na API e obtém token"""
        try:
            url = f'{self.base_url}/auth/login'
            print(f"🔗 Conectando à API: {url}")
            
            payload = {'email': email, 'password': password}
            
            # Primeiro, vamos testar se a rota de login está acessível
            test_response = self.session.get(url, timeout=5)
            print(f"📡 Teste pré-login: Status {test_response.status_code}")
            
            # Agora faz o login
            response = self.session.post(
                url,
                json=payload,
                timeout=15  # Timeout maior para login
            )
            
            print(f"📡 Status do login: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                print("✅ Login realizado com sucesso!")
                if self.token:
                    print(f"🔑 Token recebido: {self.token[:50]}...")
                return True, data
            else:
                error_msg = response.json().get('error', f'HTTP {response.status_code}')
                print(f"❌ Erro no login: {error_msg}")
                return False, {'error': error_msg}
                
        except requests.exceptions.Timeout:
            error = 'Timeout - API demorou para responder'
            print(f"❌ {error}")
            return False, {'error': error}
        except requests.exceptions.ConnectionError:
            error = 'Erro de conexão - Verifique a URL da API'
            print(f"❌ {error}")
            return False, {'error': error}
        except Exception as e:
            error = f'Erro inesperado: {str(e)}'
            print(f"❌ {error}")
            return False, {'error': error}
    
    def _make_request(self, method, endpoint, data=None, retry_count=2):
        """Método genérico para requests com retry"""
        for attempt in range(retry_count + 1):
            try:
                url = f'{self.base_url}{endpoint}'
                print(f"🌐 Request {attempt+1}/{retry_count+1}: {method} {url}")
                
                headers = self._get_headers()
                
                if method.upper() == 'GET':
                    response = self.session.get(url, headers=headers, timeout=10)
                else:
                    response = self.session.request(method, url, json=data, headers=headers, timeout=10)
                
                print(f"📡 Response status: {response.status_code}")
                
                if response.status_code in [200, 201]:
                    return True, response.json()
                elif response.status_code == 401:
                    return False, {'error': 'Não autorizado - Token inválido'}
                elif response.status_code == 403:
                    return False, {'error': 'Acesso negado - Permissões insuficientes'}
                elif response.status_code == 404:
                    return False, {'error': 'Endpoint não encontrado'}
                else:
                    error_msg = response.json().get('error', f'HTTP {response.status_code}')
                    return False, {'error': error_msg}
                    
            except requests.exceptions.Timeout:
                if attempt < retry_count:
                    print(f"⏳ Timeout, tentando novamente... ({attempt + 1}/{retry_count})")
                    time.sleep(1)
                else:
                    return False, {'error': 'Timeout após várias tentativas'}
            except requests.exceptions.ConnectionError:
                if attempt < retry_count:
                    print(f"🔌 Connection error, tentando novamente... ({attempt + 1}/{retry_count})")
                    time.sleep(1)
                else:
                    return False, {'error': 'Erro de conexão após várias tentativas'}
            except Exception as e:
                return False, {'error': f'Erro: {str(e)}'}
    
    # Métodos específicos
    def get_products(self):
        return self._make_request('GET', '/products')
    
    def get_admin_stats(self):
        return self._make_request('GET', '/admin/stats')
    
    def get_all_orders(self):
        return self._make_request('GET', '/admin/orders')
    
    def get_all_users(self):
        return self._make_request('GET', '/admin/users')
    
    def get_live_deliveries(self):
        return self._make_request('GET', '/admin/deliveries/live')

# Instância global
api_client = EcoGasAPI()