from django.urls import path
from . import views


app_name='core'


urlpatterns=[
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.log_in,name='login'),
    path('login/',views.logOut,name='logout'),
    path('signup/',views.signup,name='signup')
]
