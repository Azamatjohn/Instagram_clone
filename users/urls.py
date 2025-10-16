
from .views import CreateUserView, VerifyAPIView, GetNewCodeView, ChangeUserInformationView, ChangeUserPhotoView, \
    LoginAPIView,LoginRefreshView, LogoutAPIView, ForgotPasswordAPIView, ResetPasswordAPIView
from django.urls import path



urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login/refresh/', LoginRefreshView.as_view(), name='refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('verify/', VerifyAPIView.as_view(), name='verify'),
    path('newcode/', GetNewCodeView.as_view(), name='newcode'),
    path('change-user/', ChangeUserInformationView.as_view(), name='change-user'),
    path('change-photo/', ChangeUserPhotoView.as_view(), name='change-photo'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
]