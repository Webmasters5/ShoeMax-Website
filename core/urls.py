from django.urls import path
from . import views
from .views import forgot_password_view
from django.contrib.auth import views as auth_views

app_name='core'


urlpatterns=[
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.log_in,name='login'),
    path('login/',views.logOut,name='logout'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('signup/',views.signup,name='signup'),
    # path('forgot/',views.forgot_password_view,name='forgot'),

    path('password_reset/', forgot_password_view.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
