from django.contrib.auth import get_backends, get_user_model
from django.contrib.auth.backends import ModelBackend

from web_project.apps.accounts import MyLDAPBackend


"""
Backend de autenticación clásica
Anulamos django.contrib.custom_auth.backends.ModelBackend para garantizar que los usuarios ldap no puedan iniciar sesión 
con este si MyLDAPBackend está disponible.
"""

class MyAuthBackend(ModelBackend):
    """ A custom authentication backend overriding django ModelBackend """

    @staticmethod
    def _is_ldap_backend_activated():
        """ Returns True if MyLDAPBackend is activated """
        return MyLDAPBackend in [b.__class__ for b in get_backends()]

    def authenticate(self, username, password):
        """ Overrides ModelBackend to refuse LDAP users if MyLDAPBackend is activated """

        if self._is_ldap_backend_activated():
            user_model = get_user_model()
            try:
                user_model.objects.get(username=username, from_ldap=False)
            except:
                return None

        user = ModelBackend.authenticate(self, username, password)

        return user