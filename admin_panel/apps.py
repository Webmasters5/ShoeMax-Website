from django.contrib.admin.apps import AdminConfig

class AdminPanelConfig(AdminConfig):
    default_site = 'admin_panel.admin.ShoeMaxAdmin'