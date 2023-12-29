from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.core.cache import cache
from .models import BlockedIP
from .conf import settings

class BlockedIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        context = {
            "ip_address": ip_address,
        }

        # if ip_address is not None:
        #     try:
        #         blocked_ip = BlockedIP.objects.get(ip_address=ip_address)
        #         if settings.BLOCKED_IP_TEMPLATE:
        #             return render(request, settings.BLOCKED_IP_TEMPLATE, context, status=403)
        #
        #         raise PermissionDenied("You have been blocked from this site.")
        #     except BlockedIP.DoesNotExist:
        #         pass

        if ip_address is not None:
            blocked_ip = cache.get(ip_address)
            if blocked_ip is not None:
                if settings.BLOCKED_IP_TEMPLATE:
                    return render(request, settings.BLOCKED_IP_TEMPLATE, context, status=403)
                raise PermissionDenied("You have been blocked from this site.")
            else:
                blocked_ip = BlockedIP.objects.filter(ip_address=ip_address).first()
                if blocked_ip is not None:
                    cache.set(ip_address, blocked_ip)


        response = self.get_response(request)
        return response
