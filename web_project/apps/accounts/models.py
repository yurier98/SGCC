from django.contrib.auth.models import AbstractUser, User
from django.db import models


class Perfil(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='perfil', on_delete=models.CASCADE)
    solapin = models.CharField(max_length=7)
    nombre = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=40)
    categoria = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    foto = models.URLField(max_length=110)


    class Meta:
        permissions = (
            ('administrador', 'Es Administrador'),
            ('dependiente', 'Es Dependiente'),
            ('contador', 'Es Contador'),

        )
        #app_label = 'web.site_web'

    def __str__(self):
        return str(self.nombre)




