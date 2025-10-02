from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .client import api_client

class APIAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(f"🔐 Tentando autenticar: {username}")
        
        success, response = api_client.login(username, password)
        
        if success:
            try:
                user_data = response.get('user', {})
                
                # Busca ou cria usuário
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': username,
                        'first_name': user_data.get('name', ''),
                        'is_staff': True,
                        'is_active': True
                    }
                )
                
                if created:
                    user.set_unusable_password()
                    user.save()
                    print(f"✅ Novo usuário criado: {username}")
                else:
                    print(f"✅ Usuário existente: {username}")
                
                # Armazena dados da API na sessão
                request.session['api_token'] = response.get('token')
                request.session['user_data'] = user_data
                request.session['is_authenticated_via_api'] = True
                
                return user
                
            except Exception as e:
                print(f"❌ Erro ao criar usuário: {e}")
                return None
        else:
            print(f"❌ Falha na autenticação API: {response.get('error')}")
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None