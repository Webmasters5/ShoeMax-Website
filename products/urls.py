from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'products'

urlpatterns = [
    path('search/', views.search, name='search'),
    path('<int:shoe_id>/', views.shoe_details, name='shoe_details'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('wishlist/delete/<int:item_id>/', views.delete_wishlist_item, name='wishlist_delete'),
    path('wishlist/add/<int:shoe_id>/', views.add_wishlist_item, name='wishlist_add'),
    path('dummy/',views.dummy,name='dummy'), #to delete
    path('review/<int:shoe_id>',views.reviews, name='reviews'),
    path('review/add/<int:shoe_id>',views.add_review, name='add_review'),
    path('review/edit/<int:review_id>/', views.edit_review, name='edit_review'),
]

#Images don't load without this configuration in debug mode:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)