from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.db.models import Sum, Count

# add model imports
from models_app.models import Customer, Order, OrderItem

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
        # compute statistics
        total_customers = Customer.objects.count()
        orders_qs = Order.objects.all()
        total_orders = orders_qs.count()

        # status counts and percentages
        status_counts = orders_qs.values('status').annotate(count=Count('id'))
        # normalize into a dict for template
        status_summary = {}
        for entry in status_counts:
            name = entry['status'] or 'Unknown'
            cnt = entry['count']
            pct = (cnt / total_orders * 100) if total_orders else 0
            status_summary[name] = {
                'count': cnt,
                'percent': round(pct, 1)
            }

        # total sales (sum of total_price)
        total_sales = orders_qs.aggregate(total=Sum('total_price'))['total'] or 0

        # most sold items (aggregate by OrderItem.product_name)
        most_sold_qs = (
            OrderItem.objects
            .values('product_name')
            .annotate(total_sold=Sum('quantity'))
            .order_by('-total_sold')[:10]
        )
        most_sold = list(most_sold_qs)

        context = self.each_context(request)
        context.update({
            'total_customers': total_customers,
            'total_orders': total_orders,
            'status_summary': status_summary,
            'total_sales': total_sales,
            'most_sold': most_sold,
        })

        return TemplateResponse(request, "admin/dashboard.html", context)
    
    def get_urls(self):
        urls = super().get_urls()

        print(urls)
        url_patterns = [
            path("", self.admin_view(self.dashboard_view), name="dashboard"),
        ] 
        return url_patterns + urls

