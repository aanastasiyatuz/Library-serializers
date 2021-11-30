from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import RegistrationView, LoginView, LogoutView, ActivateView, ForgotPassword, ForgotPasswordComplete

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('activate/<str:activation_code>/', ActivateView.as_view()),
    path('forgot_password/', ForgotPassword.as_view()),
    path('forgot_password_complete/<str:activation_code>/', ForgotPasswordComplete.as_view()),
]