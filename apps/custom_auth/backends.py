from django_auth_ldap.backend import LDAPBackend, _LDAPUser
from django.contrib.auth import get_user_model
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
from django.conf import settings
from django.contrib.auth.models import User
# from apps.accounts.models import UserProfile

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
    'solapin': 'postofficebox',
    'ocupacion': 'title',
    'facultad': 'department',
    'foto': 'thumbnailphoto',
    'LOGON_COUNT': 'logoncount',

    'area': 'department',
    # 'phone': 'telephoneNumber',
    'phone': 'otherTelephone',
}
# This is the default, but I like to be explicit.
settings.UTH_LDAP_ALWAYS_UPDATE_USER = True
# settings.AUTH_LDAP_USER_ATTR_MAP = bind_user_params


# Cache distinguished names and group memberships for an hour to minimize
# LDAP traffic.
settings.AUTH_LDAP_CACHE_TIMEOUT = 3600


class MyLDAPBackend(LDAPBackend):
    """ A custom LDAP authentication backend """

    def authenticate_ldap_user(self, username, password):
        """ Overrides LDAPBackend.authenticate to save user password in django """
        self.DN_NOMBRE_USUARIO_LDAP = 'givenname'
        self.DN_APELLIDO_USUARIO_LDAP = 'sn'
        self.DN_SOLAPIN_USUARIO_LDAP = 'postofficebox'
        self.DN_CORREO_USUARIO_LDAP = 'mail'
        self.DN_OCUPACION_USUARIO_LDAP = 'title'
        self.DN_FACULTAD = 'department'
        self.DN_FOTO_LDAP = 'thumbnailphoto'
        self.DN_LOGON_COUNT = 'logoncount'

        # listado con los atributos
        self.DATOS_USUARIO_LDAP = [
            self.DN_NOMBRE_USUARIO_LDAP,
            self.DN_APELLIDO_USUARIO_LDAP,
            self.DN_SOLAPIN_USUARIO_LDAP,
            self.DN_CORREO_USUARIO_LDAP,
            self.DN_OCUPACION_USUARIO_LDAP,
            self.DN_FACULTAD,
            self.DN_FOTO_LDAP,
            self.DN_LOGON_COUNT,

        ]

        self.conexion = None

        user = LDAPBackend.authenticate_ldap_user(self, username, password)

        # If user has successfully logged, save his password in django database
        if user:
            # try:
            #     ent = self.Obtener_Resultado(username)
            #     print(ent)
            # except:
            #     return None
            # if ent[0]:
            #     try:
            #
            #         perfil = UserProfile(user=user, solapin=self.getSolapin(), nombre=self.getNombre(),
            #                              apellidos=self.getApellidos(), categoria=self.getCategoria(),
            #                              area=self.getArea(), foto=self.getFoto())
            #         perfil.save()
            #
            #     except:
            #         pass

            user.set_password(password)
            user.save()

        return user

    def get_or_create_user(self, username, ldap_user):
        """ Overrides LDAPBackend.get_or_create_user to force from_ldap to True """
        kwargs = {
            'username': username,
            'defaults': {'from_ldap': True}
        }
        user_model = get_user_model()
        return user_model.objects.get_or_create(**kwargs)




    def Obtener_Resultado(self, username, **kwargs):
        """Dado un nombre de usuario, devuelve todos sus datos y su cn"""
        print('Obteniendo resultados de busqueda ...... ')
        resultados = _LDAPUser._load_user_attrs()

        print(resultados)

        try:
            resultado = LDAPSearch(ldap_user_search, ldap.SCOPE_SUBTREE,
                                   'sAMAccountName=' + username, self.DATOS_USUARIO_LDAP)
            print(resultado)
            # resultado_busqueda = self.conexion.search_s(self.CONTEXTO, ldap.SCOPE_SUBTREE,
            #                                             'sAMAccountName=' + usuario, self.DATOS_USUARIO_LDAP)
            return resultado[0]
        except:
            pass


def busquedaAuto(f):
    def wrapper(*arg):
        if len(arg) == 1:
            return f(arg[0], arg[0].autenticadoDatos)
        else:
            return f(arg[0], arg[1])

    return wrapper


@busquedaAuto
def getSolapin(self, busqueda):
    if busqueda:
        return busqueda['postOfficeBox'][0]
    return False


@busquedaAuto
def getApellidos(self, busqueda):
    if busqueda:
        return busqueda['sn'][0]
    return False


@busquedaAuto
def getNombre(self, busqueda):
    if busqueda:
        return busqueda['givenName'][0]
    return False


@busquedaAuto
def getCorreo(self, busqueda):
    if busqueda:
        return busqueda['mail'][0]
    return False


@busquedaAuto
def getCategoria(self, busqueda):
    if busqueda:
        return busqueda['title'][0]
    return False


@busquedaAuto
def getArea(self, busqueda):
    if busqueda:
        return busqueda['department'][0]
    return False


@busquedaAuto
def getFoto(self, busqueda):
    if busqueda:
        foto = "http://directorio.uci.cu/sites/all/modules/custom/directorio_de_personas/display_foto.php?id=" + self.getSolapin(
            busqueda)
        return foto
    return False


def get_user(self, user_id):
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None


from django.contrib.auth import get_backends, get_user_model
from django.contrib.auth.backends import ModelBackend


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
