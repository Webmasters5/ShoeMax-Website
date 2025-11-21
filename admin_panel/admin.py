from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path

class ShoeMaxAdmin(admin.AdminSite):
    site_header = "ShoeMax Admin Site"
    site_title = "ShoeMax Admin Site"
    logout_template = 'admin/logout.html'
    
    def each_context(self, request):
        context = super().each_context(request)
        context['username'] = request.user.get_username
        return context
    
    def dashboard_view(self, request):
        request.current_app = self.name
        context = self.each_context(request)
        return TemplateResponse(request,"admin/dashboard.html", context)
    
    def get_urls(self):
        urls = super().get_urls()

        print(urls)
        url_patterns = [
            path("", self.admin_view(self.dashboard_view), name="dashboard"),
        ] 
        return url_patterns + urls
            
