from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.forms import model_to_dict

from config.settings import base
from crum import get_current_request


class UserProfile(AbstractUser):
    """
    Modelo que representa el perfil del usuario
    """
    image = models.ImageField(verbose_name="Imagen de perfil", upload_to='users/%Y/%m/%d', null=True, blank=True,
                              default='no_picture.svg')
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)
    solapin = models.CharField(max_length=7)
    area = models.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{8,11}$',
                                 message="El número de teléfono debe ingresarse en el formato: '+5399999999'. de hasta "
                                         "11 dígitos permitidos.")
    phone = models.CharField(validators=[phone_regex], max_length=10, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def get_image(self):
        if self.image:
            return f'{base.MEDIA_URL}{self.image}'
        return f'{base.STATIC_URL}/no_picture.svg'


    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions', 'last_login'])
        item['last_login'] = '' if self.last_login is None else self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['phone'] = str(self.phone)
        item['image'] = self.get_image()
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass
