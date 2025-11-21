from django.contrib import admin
from django.contrib.auth.models import User, Group

class ShoeMaxAdmin(admin.AdminSite):
    site_header = "ShoeMax Administration"

""" admin_site = ShoeMaxAdmin(name='shoemax_admin')

# Register your models here.
admin_site.register(User)
admin_site.register(Group)
"""