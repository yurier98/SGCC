# from .models import *
# from django.contrib.postgres.fields import JSONField

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# from ...audit.utils import PrintableModel
from django.forms import model_to_dict

# from ..audit.utils import PrintableModel
# from ..managers import UserProfileManager
from .managers import UserProfileManager


# from ..models import Menu


class UserProfile(models.Model):
    """Modelo que representa el perfil del usuario"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", verbose_name="Usuario", unique=True
    )
    first_name = models.CharField('Nombre',max_length=20)
    last_name = models.CharField('Apellidos',max_length=40)
    email = models.EmailField('email address', blank=True)
    solapin = models.CharField(max_length=7)


    photo = models.URLField(verbose_name="Imagen de perfil", max_length=110, default='no_picture.svg')

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                 message=" El número de teléfono debe ingresarse en el formato: '+999999999'. de hasta 12 dígitos permitidos.")
    phone = models.CharField(validators=[phone_regex], max_length=10, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # entry_point = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    area = models.CharField(max_length=50)


    # photo = models.ImageField(upload_to="user_profile_pictures")
    # ldap = models.BooleanField(default=False, verbose_name="¿Autenticación por LDAP?")
    # ip_addres = models.CharField(max_length=15, default="255.255.255.255", verbose_name="Dirección IP permitida")
    # default_page_size = models.IntegerField(
    #     choices=[
    #         ("10", "10"),
    #         ("20", "20"),
    #         ("50", "50"),
    #         ("100", "100"),
    #         ("200", "200"),
    #         ("500", "500"),
    #     ],
    #     default=20,
    # )

    # current_login_status = models.BooleanField(
    #     default=False, verbose_name="¿Actualmente logueado?"
    # )  # False -> Deslogueado...
    # current_ip_address = models.CharField(
    #     max_length=15, null=True, blank=True, verbose_name="Dirección IP actual"
    # )
    # current_failed_login_attemps = models.IntegerField(
    #     default=0, verbose_name="Cantidad de intentos de inicio de sesión fallidos"
    # )
    # be_notified = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
        db_table = "account_user_profile"
        default_permissions = ("add", "change", "delete", "read")

    def __str__(self):
        # return f"Perfil de usuario de {self.user.first_name} {self.user.last_name}"
        return self.user.username

    def toJSON(self):
        item = model_to_dict(self, exclude=['photo'])
        item['username'] = self.user.username
        return item


class Servidor(models.Model):
    """Modelo que representa los servidores de autenticación LDAP utilizados
     #bind_user_params = JSONField(default=dict)"""
    denominacion = models.CharField(max_length=250)
    url = models.CharField(max_length=250)
    ldap_bind_dn = models.CharField(max_length=250)
    ldap_bind_password = models.CharField(max_length=250)
    ldap_user_search = models.CharField(max_length=250)
    ldap_user_search_scope_tree = models.CharField(max_length=250)
    active = models.BooleanField(default=False)

    class Meta:
        db_table = 'account_servidor'
        default_permissions = ('add', 'change', 'delete', 'read')
