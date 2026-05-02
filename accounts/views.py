from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import signupform, loginform
from .serializers import RegisterSerializer, LoginSerializer

User = get_user_model()

# Create your views here.
##      login 
def log_in(request):

    next_param = request.GET.get('next') or request.POST.get('next') or ''
    if request.method == "POST":
        form = loginform(request,data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get("remember_me")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                messages.success(request,'You have successfully logged in.')
                # Validate next; fallback to LOGIN_REDIRECT_URL
                if next_param:
                    return redirect(next_param)
                return redirect(settings.LOGIN_REDIRECT_URL or 'storefront:home')
            else:
                messages.error(request,'Error. User does not exist.')

            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)
        else:
            messages.success(request,"There was an error logging in.") 
    else:
        form = loginform()

    return render(request,"accounts/login.html", {"loginform" : form, "next": next_param})
    

###           logout
def logOut(request):
    logout(request)
    messages.success(request,"You have successfully logged out.")
    return redirect('storefront:home')


#######   sign up
def signup(request):
    if request.method == 'POST':
        form = signupform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has successfully been created.')
            return redirect('accounts:login')  # or your dashboard
    else:
        form = signupform()

    return render(request,"accounts/signup.html", {'form' : form})



############# FORGOT PASSWORD ##########################


class forgot_password_view(PasswordResetView):
    template_name = "registration/password_reset_form.html"
    email_template_name = "registration/password_reset_email.html"
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            "domain": "localhost:8000",  # change in prod (e.g., myapp.com)
            "protocol": "http",          # use "https" in production
        })
        return ctx


# REGISTER
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# LOGIN
class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"]
        )
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# LOGOUT
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the user's token to "log them out"
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


# FORGOT PASSWORD
class ForgotPasswordView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f"http://127.0.0.1:8000/accounts/reset/{uid}/{token}/"
        send_mail(
            "Password Reset",
            f"Click the link to reset your password: {reset_link}",
            "noreply@shoemax.com",
            [email],
        )
        return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)
