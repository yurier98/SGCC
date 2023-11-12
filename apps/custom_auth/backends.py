import threading
from urllib import request

from django_auth_ldap.backend import LDAPBackend, _LDAPUser
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
from django.conf import settings
from django.contrib.auth.models import User

"""
Back-end de autenticación LDAP
Este backend LDAP tiene dos objetivos:

Guarde la contraseña del usuario en la base de datos de django, por lo que podrá iniciar sesión en django si
el backend de autenticación LDAP está deshabilitado;
Forzar from_ldap campo a True cuando se crea un usuario de esta manera.

"""

"""
    Se definen varias configuraciones de autenticación LDAP en la configuración de Django utilizando 
    settings.AUTH_LDAP_*. Esto incluye la URL del servidor LDAP, el usuario y contraseña para la conexión LDAP, 
    así como los atributos de usuario a mapear con los campos de usuario en Django.
"""

# Si la conexión LDAP no se establece en 10 segundos, Django utilizará la autenticación interna en lugar de intentar
# conectarse al servidor LDAP. Esto ayudará a evitar retrasos prolongados cuando el servidor LDAP esté caído.
# Configuración de timeout
ldap.set_option(ldap.OPT_NETWORK_TIMEOUT, 10)

# settings.AUTH_LDAP_CONNECTION_OPTIONS = {
#     ldap.OPT_NETWORK_TIMEOUT: 5
# }

# Configuración de conexión LDAP
settings.AUTH_LDAP_SERVER_URI = 'ldap://10.0.0.4'
settings.AUTH_LDAP_BIND_DN = 'cn=ad search, ou=Systems, ou=UCI Domain Impersonals, dc=uci, dc=cu'
settings.AUTH_LDAP_BIND_PASSWORD = 'uF2SODWAHiW0eJboFFQEAvVzJ'

# Configuración de búsqueda de usuarios LDAP
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
    """ A custom LDAP authentication backend
        El MyLDAPBackend es un backend personalizado que extiende el LDAPBackend proporcionado por django_auth_ldap.
        Este backend anula el método authenticate_ldap_user para guardar la contraseña del usuario en la base de datos
        de Django después de que la autenticación LDAP tenga éxito.
        """

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

        # Inicia un hilo de autenticación LDAP
        auth_thread = threading.Thread(target=LDAPBackend.authenticate_ldap_user, args=(self, username, password))
        auth_thread.start()

        # Espera hasta 10 segundos para que el hilo de autenticación termine
        auth_thread.join(timeout=10)

        # Comprueba si el hilo de autenticación aún está en ejecución (es decir, ha superado el límite de tiempo)
        if auth_thread.is_alive():
            # Si el hilo de autenticación LDAP todavía está en ejecución después de 10 segundos, entonces recurre al método de autenticación de Django
            user = ModelBackend().authenticate(request, username=username, password=password)
            if user is not None:
                # Guarda la contraseña en la base de datos de Django si el usuario ha iniciado sesión correctamente
                user.set_password(password)
                user.save()
                return user
        else:
            # Si el hilo de autenticación LDAP ha terminado, procede como lo haría normalmente en tu método de autenticación
            user = LDAPBackend.authenticate_ldap_user(self, username, password)
            if user:
                user.set_password(password)
                user.save()
                return user

        return None

        # self.conexion = None
        #
        # user = LDAPBackend.authenticate_ldap_user(self, username, password)
        # # If user has successfully logged, save his password in django database
        # if user:
        #     # try:
        #     #     ent = self.Obtener_Resultado(username)
        #     #     print(ent)
        #     # except:
        #     #     return None
        #     # if ent[0]:
        #     #     try:
        #     #         perfil = UserProfile(user=user, solapin=self.getSolapin(), nombre=self.getNombre(),
        #     #                              apellidos=self.getApellidos(), categoria=self.getCategoria(),
        #     #                              area=self.getArea(), foto=self.getFoto())
        #     #         perfil.save()
        #     #     except:
        #     #         pass
        #     user.set_password(password)
        #     user.save()
        #
        # return user

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
        """ Overrides ModelBackend to refuse LDAP users if MyLDAPBackend is activated
        Este backend se utiliza para evitar que los usuarios autenticados mediante LDAP inicien sesión si el backend
        de autenticación LDAP está activado. En otras palabras, solo se permitirá el inicio de sesión para usuarios
        que no provengan de LDAP si el backend LDAP está activado.
        """

        if self._is_ldap_backend_activated():
            user_model = get_user_model()
            try:
                user_model.objects.get(username=username, from_ldap=False)
            except:
                return None

        user = ModelBackend.authenticate(self, username, password)

        return user
