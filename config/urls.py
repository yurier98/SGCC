"""web_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from apps.core import views

handler403 = views.custom_permission_denied_view

urlpatterns = [

    # URL para hacer la app compatible con pwa
    path('', include('config.pwa1.urls')),

    path('', include('apps.core.urls')),
    path('', include('apps.custom_auth.urls')),
    path('nomenclatures/', include('apps.nomenclatures.urls')),
    path('accounts/', include('apps.accounts.urls')),

    path('inventory/', include('apps.inventory.urls')),
    path('loan/', include('apps.loan.urls')),
    path('order/', include('apps.order.urls')),

    path('notification/', include('apps.notification.urls')),
    path('reports/', include(('apps.reports.urls', 'reports'))),

    path('security/', include('apps.security.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
