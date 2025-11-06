from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from products.models import Shoe
from django.views.generic import ListView

def home(request):
    context={
        'active_class':'home'
    }
    return render(request,'homepage/home.html',context)


class ProductsByGenderView(ListView):
    model = Shoe
    template_name = 'homepage/prod_gender.html' 
    paginate_by = 8

    def get_queryset(self):
        gender = self.kwargs.get('gender')
        return Shoe.objects.filter(Q(gender=gender) | Q(gender='U'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gender'] = self.kwargs.get('gender')
        context['active_class'] = self.kwargs.get('gender')

        return context

def category(request,category):
    if category=="trainers":
        shoes=Shoe.objects.filter(Q(category="running")|Q(category="sports")|Q(category="casual")|Q(category="sneakers")|Q(category="athletic"))
    elif category=="formals":
        shoes=Shoe.objects.filter(Q(category="formal")|Q(category="loafers"))
    elif category=="crocs":
        shoes=Shoe.objects.filter(category="crocs")
    elif category=="dress-shoes":
        shoes=Shoe.objects.filter(Q(category="heels")|Q(category="dress pumps"))
    elif category=="sandals":
        shoes=Shoe.objects.filter(category="sandals")
    elif category=="boots":
        shoes=Shoe.objects.filter(category="boots")
    context={
        'shoes':shoes,
        'category':category,
    }
    return render(request,'homepage/categories.html',context)