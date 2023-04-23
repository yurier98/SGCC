# project/settings.py
import os.path
from .base import BASE_DIR

PWA_APP_NAME = 'GEPRE'
PWA_APP_DESCRIPTION = "Sistema para la gestión de préstamos en la Dirección de Extensión Universitaria de la UCI "
PWA_APP_THEME_COLOR = '#266867'
PWA_APP_BACKGROUND_COLOR = '#266867'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        # 'src': '/static/images/my_app_icon.png',
        'src': 'static/assets/images/my_app_icon.png',
        'sizes': '160x160'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': 'static/assets/images/my_apple_icon.png',
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        # 'src': '/static/images/icons/splash-640x1136.png',
        'src': 'static/assets/images/doc-thumb-2.jpg',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'es'

PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, "static/assets/js/serviceworker.js")
