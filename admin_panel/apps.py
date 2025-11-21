"""
from django.apps import AppConfig

class AdminPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_panel'
 """
from django.contrib.admin.apps import AdminConfig

class AdminPanelConfig(AdminConfig):
    default_site = 'admin_panel.admin.ShoeMaxAdmin'