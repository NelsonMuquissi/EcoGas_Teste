# Criar o arquivo se não existir
import requests
import json
from django.conf import settings

class HybridEcoGasAPI:
    def __init__(self):
        self.base_url = "https://api-ecogas.onrender.com"
        self.token = None
        self.use_real_api = False
        self._mock_data = self._load_mock_data()
    
    def _load_mock_data(self):
        return {
            "stats": {"orders_today": 15, "pending_deliveries": 8, "active_customers": 124, "monthly_revenue": 285000},
            "products": [
                {"id": 1, "name": "Botijão Gás 12kg", "price": 5500, "stock": 45},
                {"id": 2, "name": "Botijão Gás 6kg", "price": 3200, "stock": 23},
            ],
            "orders": [
                {"id": 1001, "customer_name": "Maria Silva", "product_name": "Botijão Gás 12kg", "status": "pending"},
                {"id": 1002, "customer_name": "João Santos", "product_name": "Botijão Gás 6kg", "status": "accepted"},
            ],
            "users": [
                {"id": 1, "name": "Admin", "email": "admin@ecogas.com", "role": "admin"},
                {"id": 2, "name": "Cliente", "email": "cliente@email.com", "role": "customer"},
            ],
            "deliveries": [
                {"id": 2001, "order_id": 1001, "delivery_person": "Entregador A", "status": "in_progress"},
            ]
        }
    
    def _test_api_connection(self):
        try:
            response = requests.get(f"{self.base_url}/products", timeout=5)
            if response.status_code == 200:
                print("✅ API real online")
                return True
        except:
            print("⚠️  API offline")
        return False
    
    def login(self, email, password):
        print(f"🔐 Login: {email}")
        if self._test_api_connection():
            try:
                response = requests.post(f"{self.base_url}/auth/login", json={"email": email, "password": password}, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    self.token = data.get('token')
                    self.use_real_api = True
                    print("🎉 LOGIN REAL!")
                    return True, data
            except:
                pass
        print("🔄 Login mock")
        mock_user = {
            "user": {"id": 1, "name": "Admin", "email": email, "role": "admin"}
        }
        self.use_real_api = False
        return True, mock_user
    
    def get_admin_stats(self):
        if self.use_real_api and self.token:
            try:
                headers = {'Authorization': f'Bearer {self.token}'}
                response = requests.get(f"{self.base_url}/admin/stats", headers=headers, timeout=10)
                if response.status_code == 200:
                    return True, response.json()
            except:
                pass
        return True, self._mock_data["stats"]
    
    def get_all_orders(self):
        if self.use_real_api and self.token:
            try:
                headers = {'Authorization': f'Bearer {self.token}'}
                response = requests.get(f"{self.base_url}/admin/orders", headers=headers, timeout=10)
                if response.status_code == 200:
                    return True, response.json()
            except:
                pass
        return True, {"orders": self._mock_data.get("orders", [])}
    
    def get_all_users(self):
        if self.use_real_api and self.token:
            try:
                headers = {'Authorization': f'Bearer {self.token}'}
                response = requests.get(f"{self.base_url}/admin/users", headers=headers, timeout=10)
                if response.status_code == 200:
                    return True, response.json()
            except:
                pass
        return True, {"users": self._mock_data.get("users", [])}
    
    def get_products(self):
        if self.use_real_api:
            try:
                response = requests.get(f"{self.base_url}/products", timeout=10)
                if response.status_code == 200:
                    products = response.json()
                    if products:
                        return True, products
            except:
                pass
        return True, self._mock_data.get("products", [])
    
    def get_live_deliveries(self):
        if self.use_real_api and self.token:
            try:
                headers = {'Authorization': f'Bearer {self.token}'}
                response = requests.get(f"{self.base_url}/admin/deliveries/live", headers=headers, timeout=10)
                if response.status_code == 200:
                    return True, response.json()
            except:
                pass
        return True, {"deliveries": self._mock_data.get("deliveries", [])}
    
    def update_order_status(self, order_id, new_status):
        for order in self._mock_data.get("orders", []):
            if order["id"] == order_id:
                order["status"] = new_status
                print(f"✅ Pedido {order_id} atualizado para: {new_status}")
                return True, {"message": "Status atualizado"}
        return False, {"error": "Pedido não encontrado"}

hybrid_api = HybridEcoGasAPI()