from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('search/', views.search, name='search'),
    path('<int:product_id>/', views.product_details, name='product_details'),
    path('dummy/',views.dummy,name='dummy'), #to delete
    path('review/<int:product_id>',views.reviews, name='reviews'),
    path('reviewform/<int:product_id>',views.review_product, name='review_product'),
]