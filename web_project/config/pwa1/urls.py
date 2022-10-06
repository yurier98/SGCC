from django.urls import re_path as url
from pwa.views import service_worker, manifest, offline

# from .views import manifest, service_worker, offline


# Serve up serviceworker.js and manifest.json at the root
urlpatterns = [
    url(r'^serviceworker\.js$', service_worker, name='serviceworker'),
    url(r'^manifest\.json$', manifest, name='manifest'),
    url('^offline/$', offline, name='offline')
]