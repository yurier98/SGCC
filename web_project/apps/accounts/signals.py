# For communication between models
from .backends import MyLDAPBackend as ldap
from .models import UserProfile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    print(sender)
    print(instance)
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print('el usuario es: ' + str(instance))
        username = instance

        ent = ldap.Obtener_Resultado(username)
        print(ent)
        print('Obtener_Resultado...... ')

        try:
            usuario = User.objects.get(username__exact=username)
            print('el usuario segundo es: ' + str(username))
            perfil = UserProfile(user=usuario, solapin=ldap.getSolapin(), nombre=ldap.getNombre(),
                                 apellidos=ldap.getApellidos(), categoria=ldap.getCategoria(),
                                 area=ldap.getArea(), foto=ldap.getFoto())
            print('el perfil es: ' + perfil)
            perfil.save()
        except:
            pass
