from django.urls import path
from . import views
from .views import ProductsByGenderView
app_name='homepage'
urlpatterns=[
    path('',views.home,name='home'),
    path('gender/<str:gender>/',ProductsByGenderView.as_view(),name='prod_by_gender'),
    path('category/<str:category>/',views.category,name='categories')
]