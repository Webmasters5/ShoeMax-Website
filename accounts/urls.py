from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import RegisterView, LoginView, LogoutView, ForgotPasswordView

app_name = "accounts"

urlpatterns = [
    # --- HTML views (UI) ---
    path("login/", views.log_in, name="login"),
    path("logout/", views.logOut, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("forgot/", views.forgot_password_view.as_view(), name="forgot"),

    # Django’s built-in password reset flow (HTML templates)
    path("password_reset/", views.forgot_password_view.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # --- API endpoints (JSON) ---
    path("api/register/", RegisterView.as_view(), name="api_register"),
    path("api/login/", LoginView.as_view(), name="api_login"),
    path("api/logout/", LogoutView.as_view(), name="api_logout"),
    path("api/forgot-password/", ForgotPasswordView.as_view(), name="api_forgot_password"),
]
