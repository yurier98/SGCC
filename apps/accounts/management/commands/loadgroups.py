from django.contrib.auth.models import Group, Permission


def create_groups():
    # Crear grupos
    admin_group, created = Group.objects.get_or_create(name='administrador')
    tecnico_group, created = Group.objects.get_or_create(name='tecnico')

    # Asignar permisos a los grupos
    '''Nota:  Actualizar los permisos q va a tener el usuario administrador '''
    admin_permissions = Permission.objects.filter(codename__in=[
        'view_category',

    ])
    admin_group.permissions.set(admin_permissions)

    tecnico_permissions = Permission.objects.filter(codename__in=[
        'add_product',
        'change_product',
        'delete_product',
        'view_product',
        'report_product',

        'add_loan',
        'change_loan',
        'delete_loan',
        'view_loan',
        'report_loan',

        'approve_order',
        'view_all_order',
    ])
    tecnico_group.permissions.set(tecnico_permissions)


from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Crea grupos por defecto y les asigna permisos'

    def handle(self, *args, **options):
        create_groups()
        self.stdout.write(self.style.SUCCESS('Grupos creados con éxito!'))
