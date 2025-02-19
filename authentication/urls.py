from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (LoginAPIView, LogoutAPIView, PasswordTokenCheckAPI,
                    RegisterView, RequestPasswordResetEmail,
                    SetNewPasswordAPIView, VerifyEmail, VerifyToken)

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('signin/', LoginAPIView.as_view(), name="signin"),
    path('signout/', LogoutAPIView.as_view(), name="signout"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', VerifyToken.as_view(), name='token_verify'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete')
]