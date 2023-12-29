from datetime import timezone

from apps.loan.models import Loan
from apps.notification.signals import notificar


def chequear_prestamos(user):
    # Obtener todos los préstamos que están prestados o atrasados
    prestamos = Loan.objects.filter(order__user__id=user.id)

    for prestamo in prestamos:
        # Obtener la orden asociada al préstamo
        orden = prestamo.order

        # Calcular la cantidad de días restantes antes de la fecha de devolución
        remaining_days = (orden.end_date - timezone.now().date()).days

        if remaining_days < 0:

            notificar.send(user, user=user,
                           message='El préstamo está atrasado "{}". Por favor, devuélvalo lo antes posible.'.format(
                               orden.__str__()),
                           level='wrong')
        # Si hoy es la fecha de devolución, enviar una notificación
        elif remaining_days == 0:
            notificar.send(user, user=user,
                           message='Hoy es la fecha de devolución del préstamo "{}". Por favor, devuélvalo lo antes posible.'.format(
                               orden.__str__()),
                           level='wrong')


        # Si quedan dos días o menos para la fecha de devolución, enviar una notificación
        elif remaining_days <= 2:
            notificar.send(user, user=user,
                           message='Quedan {} días para delover el prestamo "{}"'.format(remaining_days,
                               orden.__str__()),
                           level='info')
