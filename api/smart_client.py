import requests
import json
from django.conf import settings

class SmartEcoGasAPI:
    def __init__(self):
        self.base_url = "https://api-ecogas.onrender.com"
        self.token = None
        self.use_mock = True  # Começar com mock por padrão
        self._mock_data = self._load_mock_data()
    
    def _load_mock_data(self):
        """Carrega dados mock para desenvolvimento"""
        return {
            "stats": {
                "orders_today": 15,
                "pending_deliveries": 8,
                "active_customers": 124,
                "monthly_revenue": 285000,
                "delivery_success_rate": 92
            },
            "products": [
                {
                    "id": 1,
                    "name": "Botijão Gás 12kg",
                    "description": "Gás butano para uso doméstico familiar",
                    "price": 5500,
                    "stock": 45,
                    "category": "gas",
                    "image": "/static/images/gas12kg.jpg"
                },
                {
                    "id": 2,
                    "name": "Botijão Gás 6kg",
                    "description": "Gás butano para solteiros ou pequenas famílias", 
                    "price": 3200,
                    "stock": 23,
                    "category": "gas",
                    "image": "/static/images/gas6kg.jpg"
                },
                {
                    "id": 3,
                    "name": "Botijão Gás 45kg",
                    "description": "Gás butano para uso industrial ou restaurantes",
                    "price": 18000, 
                    "stock": 12,
                    "category": "gas",
                    "image": "/static/images/gas45kg.jpg"
                }
            ],
            "orders": [
                {
                    "id": 1001,
                    "customer_name": "Maria Silva",
                    "customer_email": "maria@email.com",
                    "customer_phone": "912345678",
                    "product_name": "Botijão Gás 12kg",
                    "product_id": 1,
                    "quantity": 1,
                    "total_amount": 5500,
                    "status": "pending",
                    "created_at": "2025-09-29 10:30:00",
                    "address": "Rua das Flores, 123 - Luanda"
                },
                {
                    "id": 1002,
                    "customer_name": "João Santos", 
                    "customer_email": "joao@email.com",
                    "customer_phone": "923456789",
                    "product_name": "Botijão Gás 6kg",
                    "product_id": 2,
                    "quantity": 2, 
                    "total_amount": 6400,
                    "status": "accepted",
                    "created_at": "2025-09-29 09:15:00",
                    "address": "Avenida 4 de Fevereiro, 456 - Luanda"
                },
                {
                    "id": 1003,
                    "customer_name": "Ana Pereira",
                    "customer_email": "ana@email.com", 
                    "customer_phone": "934567890",
                    "product_name": "Botijão Gás 12kg",
                    "product_id": 1,
                    "quantity": 1,
                    "total_amount": 5500,
                    "status": "delivered",
                    "created_at": "2025-09-28 16:45:00",
                    "address": "Bairro Popular, 789 - Luanda"
                }
            ],
            "users": [
                {
                    "id": 1,
                    "name": "Administrador Sistema",
                    "email": "admin@ecogas.com",
                    "role": "admin",
                    "phone": "912345678",
                    "created_at": "2025-09-01 00:00:00"
                },
                {
                    "id": 2, 
                    "name": "Carlos Fernandes",
                    "email": "carlos@email.com",
                    "role": "customer",
                    "phone": "923456789",
                    "created_at": "2025-09-15 14:20:00"
                },
                {
                    "id": 3,
                    "name": "Sofia Mendes",
                    "email": "sofia@email.com",
                    "role": "customer", 
                    "phone": "934567890",
                    "created_at": "2025-09-20 09:30:00"
                }
            ],
            "deliveries": [
                {
                    "id": 2001,
                    "order_id": 1001,
                    "delivery_person": "Entregador A",
                    "status": "in_progress",
                    "current_location": "-8.8383, 13.2344",  # Coordenadas Luanda
                    "estimated_time": "30 minutos"
                },
                {
                    "id": 2002, 
                    "order_id": 1002,
                    "delivery_person": "Entregador B",
                    "status": "pending",
                    "current_location": "-8.8156, 13.2304",
                    "estimated_time": "45 minutos"
                }
            ]
        }
    
    def _test_api_connection(self):
        """Testa se a API real está funcionando"""
        try:
            response = requests.get(f"{self.base_url}/products", timeout=5)
            if response.status_code == 200:
                print("✅ API real está online")
                return True
        except:
            print("⚠️  API real offline, usando dados mock")
        return False
    
    def login(self, email, password):
        """Sistema de login local para desenvolvimento"""
        # Para desenvolvimento, aceita qualquer email/senha
        # Em produção, isso seria substituído pela API real
        
        mock_user = {
            "user": {
                "id": 1,
                "name": "Administrador EcoGás",
                "email": email,
                "role": "admin",
                "phone": "912345678"
            },
            "token": f"mock_jwt_token_for_{email}"
        }
        self.token = mock_user["token"]
        print(f"✅ Login mock bem-sucedido para: {email}")
        return True, mock_user
    
    # Métodos para obter dados
    def get_admin_stats(self):
        if self._test_api_connection():
            # Aqui iria a chamada real para /admin/stats
            # Por enquanto retorna mock
            pass
        return True, self._mock_data["stats"]
    
    def get_all_orders(self):
        return True, {"orders": self._mock_data["orders"]}
    
    def get_all_users(self):
        return True, {"users": self._mock_data["users"]}
    
    def get_products(self):
        return True, self._mock_data["products"]
    
    def get_live_deliveries(self):
        return True, {"deliveries": self._mock_data["deliveries"]}
    
    def update_order_status(self, order_id, new_status):
        """Atualiza status do pedido (mock)"""
        for order in self._mock_data["orders"]:
            if order["id"] == order_id:
                order["status"] = new_status
                print(f"✅ Pedido {order_id} atualizado para: {new_status}")
                return True, {"message": "Status atualizado com sucesso"}
        return False, {"error": "Pedido não encontrado"}

# Instância global
smart_api = SmartEcoGasAPI()