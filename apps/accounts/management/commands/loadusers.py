from django.contrib.auth.models import User, Group

from ...models import UserProfile



def create_group():
    # Crear grupos
    admin_group, created = Group.objects.get_or_create(name='administrador')
    tecnico_group, created = Group.objects.get_or_create(name='tecnico')
    # user_group, created = Group.objects.get_or_create(name='usuario')



def create_users():
    # Crear grupos
    admin_group, created = Group.objects.get_or_create(name='administrador')
    tecnico_group, created = Group.objects.get_or_create(name='tecnico')


    # Crear usuarios
    admin_user, created = UserProfile.objects.get_or_create(
        username='admin',
        email='admin@example.com',
        is_staff=True,
        is_superuser=True
    )
    admin_user.set_password('admin')
    admin_user.save()
    admin_user.groups.add(admin_group)

    tecnico_user, created = UserProfile.objects.get_or_create(
        username='tecnico',
        email='tecnico@example.com',
        is_staff=False,
        is_superuser=False
    )
    tecnico_user.set_password('tecnico')
    tecnico_user.save()
    tecnico_user.groups.add(tecnico_group)


from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Crea usuarios y grupos por defecto'
    help = 'Crea grupos por defecto y les asigna permisos'

    def handle(self, *args, **options):
        create_group()
        self.stdout.write(self.style.SUCCESS('Grupos creados con éxito!'))
        create_users()
        self.stdout.write(self.style.SUCCESS('Usuarios creados con éxito!'))