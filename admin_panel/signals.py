from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """
    Create default groups and attach permissions.
    This runs after migrations.
    """
    app_config = kwargs.get('app_config')
    if app_config and app_config.name != 'admin_panel':
        return

    groups_permissions = {
        'Inventory Manager': [
            ('models_app', 'view_shoe'),
            ('models_app', 'add_shoe'),
            ('models_app', 'change_shoe'),
            ('models_app', 'delete_shoe'),
            ('models_app', 'view_shoevariant'),
            ('models_app', 'add_shoevariant'),
            ('models_app', 'change_shoevariant'),
        ],
        'Pricing Manager': [
            ('models_app', 'view_shoe'),
            ('models_app', 'change_shoe'),  
            ('models_app', 'view_order'), 
        ],
        'Order Manager': [
            ('models_app', 'view_order'),
            ('models_app', 'add_order'),
            ('models_app', 'change_order'),
            ('models_app', 'delete_order'),
            ('models_app', 'view_orderitem'),
            ('models_app', 'change_orderitem'),
        ],
    }

    for group_name, perms in groups_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)
        # collect Permission queryset for this group
        perm_qs = Permission.objects.none()
        for app_label, codename in perms:
            perm_qs = perm_qs | Permission.objects.filter(content_type__app_label=app_label, codename=codename)
        group.permissions.set(perm_qs)
        group.save()