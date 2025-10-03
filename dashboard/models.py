from django.db import models
from django.contrib.auth.models import User


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    
    class Meta:
        verbose_name = 'Sessão de Usuário'
        verbose_name_plural = 'Sessões de Usuários'