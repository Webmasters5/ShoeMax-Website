from django.urls import path
from . import views

app_name='storefront'
urlpatterns=[
    path('',views.home,name='home'),
    path('categories/', views.categories, name='categories'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('brands/', views.BrandListView.as_view(), name='brand_list'),
]