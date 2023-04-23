from django_auth_ldap.backend import LDAPBackend
from django.contrib.auth import get_user_model
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
from django.conf import settings

"""
Back-end de autenticación LDAP
Este backend LDAP tiene dos objetivos:

Guarde la contraseña del usuario en la base de datos de django, por lo que podrá iniciar sesión en django si
el backend de autenticación LDAP está deshabilitado;
Forzar from_ldap campo a True cuando se crea un usuario de esta manera.

"""

settings.AUTH_LDAP_SERVER_URI = 'ldap://10.0.0.4'
settings.AUTH_LDAP_BIND_DN = 'cn=ad search, ou=Systems, ou=UCI Domain Impersonals, dc=uci, dc=cu'
settings.AUTH_LDAP_BIND_PASSWORD = 'uF2SODWAHiW0eJboFFQEAvVzJ'
ldap_user_search = 'OU=uci domain users,DC=uci,DC=cu'
ldap_user_search_scope_tree = '(sAMAccountName=%(user)s)'

settings.AUTH_LDAP_USER_SEARCH = LDAPSearch(ldap_user_search, ldap.SCOPE_SUBTREE,
                                            ldap_user_search_scope_tree)

# bind_user_params = {
#     "first_name": "pepe",
#     "last_name": "sn",
#     "email": "mail",
#     "ocupacion": "title",
#     "facultad": "department",
#     "logoncount": "logoncount",
#     "solapin": "postofficebox"
# }
settings.AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail',
}
# This is the default, but I like to be explicit.
settings.UTH_LDAP_ALWAYS_UPDATE_USER = True
# settings.AUTH_LDAP_USER_ATTR_MAP = bind_user_params


# Cache distinguished names and group memberships for an hour to minimize
# LDAP traffic.
settings.AUTH_LDAP_CACHE_TIMEOUT = 3600


class MyLDAPBackend(LDAPBackend):
    """ A custom LDAP authentication backend """

    def authenticate(self, username, password):
        """ Overrides LDAPBackend.authenticate to save user password in django """

        user = LDAPBackend.authenticate(self, username, password)

        # If user has successfully logged, save his password in django database
        if user:
            user.set_password(password)
            user.save()

        return user

    # def get_or_create_user(self, username, ldap_user):
    #     """ Overrides LDAPBackend.get_or_create_user to force from_ldap to True """
    #     kwargs = {
    #         'username': username,
    #         'defaults': {'from_ldap': True}
    #     }
    #     user_model = get_user_model()
    #     return user_model.objects.get_or_create(**kwargs)
