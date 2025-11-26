from django.contrib.admin.apps import AdminConfig

class AdminPanelConfig(AdminConfig):
    default_site = 'admin_panel.admin.ShoeMaxAdmin'
    
from django.apps import AppConfig

class AdminAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_panel'

    def ready(self):
        # ensure signals run on startup/migrations
        import admin_panel.signals