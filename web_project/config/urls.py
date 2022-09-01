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

urlpatterns = [

   # path("", include("apps.accounts.urls")),

    path('',  include('apps.core.urls')),
    path('admin/', admin.site.urls),
    # path('', views.index, name='home'),
    # path('', TemplateView.as_view(template_name="index.html"), name='home'),
    # path('inventory/', TemplateView.as_view(template_name="inventory/inventory_list.html"), name='inventory'),

    path('accounts/', include('apps.accounts.urls')),
    path('inventory/', include('apps.inventory.urls', namespace='inventory')),
    path('loan/', include('apps.loan.urls')),
    path('order/', include('apps.order.urls')),
    path('notification/', include('apps.notification.urls')),
    path('reports/', include('apps.reports.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
