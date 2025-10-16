from http.client import responses

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils import timezone
from django.views.generic import CreateView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from shared.utility import send_email, send_phone_code, check_email_or_phone
from .serializers import UserSignupSerializer, ChangeUserInformation, ChangeUserPhoto, LoginSerializer, \
    LoginRefreshSerializer, LogoutSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from .models import User, CODE_VERIFIED, NEW, VIA_EMAIL, VIA_PHONE


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.get_queryset().get(id=response.data['id'])

        refresh = RefreshToken.for_user(user)

        return Response({
            "id": user.id,
            "auth_type": user.auth_type,
            "auth_status": user.auth_status,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class VerifyAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        code = request.data.get("code")

        self.check_verify_code(user, code)

        return Response({
            "success": True,
             "auth_status": user.auth_status,
             "access_token": user.token()['access_token'],
             "refresh_token": user.token()['refresh_token']}, status=status.HTTP_200_OK)



    @staticmethod
    def check_verify_code(user, code):
        verifies = user.verify_codes.filter(expires_at__gte=timezone.now(), code=code, is_confirmed=False)
        print(verifies)
        if not verifies.exists():
            data = {
                'message': "Your code is expired or invalid.",
            }
            raise ValidationError(data)
        else:
            verifies.update(is_confirmed=True)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()

        return True



class GetNewCodeView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        user = request.user
        self.check_verification(user)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verification_code(VIA_EMAIL)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verification_code(VIA_PHONE)
            send_phone_code(user.phone_number, code)
        else:
            data = {
                "success": False,
                "message": "invalid email or phone number",
            }
            raise ValidationError(data)

        return Response({
            "success": True,
            "message": "code has been sent successfully",
        })


    @staticmethod
    def check_verification(user):
        verifies = user.verify_codes.filter(expires_at__gte=timezone.now(), is_confirmed=False)
        if verifies.exists():
            data = {
                'message': "Your code is available, please wait until it expires.",
            }
            raise ValidationError(data)

class ChangeUserInformationView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangeUserInformation
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

        return Response({
            "success": True,
            "message": "User information has been updated",
            "auth_status": self.request.user.auth_status,
        })

    def patch(self, request, *args, **kwargs):
        super().patch(request, *args, **kwargs)

        return Response({
            "success": True,
            "message": "User information has been updated",
            "auth_status": self.request.user.auth_status,
        })

class ChangeUserPhotoView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        serializer = ChangeUserPhoto(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Photo has been updated successfully",
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LoginRefreshView(TokenRefreshView):
    serializer_class = LoginRefreshSerializer

class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                "success": True,
                "message": "Login has been successfully revoked",
            }
            return Response(data, status=205)
        except TokenError:
            return Response({"success": False, "message": "Login failed"})


class ForgotPasswordAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email_or_phone = serializer.validated_data.get("email_or_phone")
        user = serializer.validated_data.get("user")
        if check_email_or_phone(email_or_phone) == "phone":
            code = user.create_verification_code(VIA_PHONE)
            send_phone_code(email_or_phone, code)
        elif check_email_or_phone(email_or_phone) == "email":
            code = user.create_verification_code(VIA_EMAIL)
            send_email(email_or_phone, code)

        return Response({
            "success": True,
            "message": "Varification code has been sent successfully",
            'access_token': user.token()['access_token'],
            'refresh_token': user.token()['refresh_token'],
            'user_status': user.auth_status,
        }, status=status.HTTP_200_OK)


class ResetPasswordAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResetPasswordSerializer
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user
    def update(self, request, *args, **kwargs):
        response = super(ResetPasswordAPIView, self).setup(request, *args, **kwargs)
        try:
            user = User.objects.get(id=self.request.user.id)
        except ObjectDoesNotExist:
            raise Http404
        return Response({
            "success": True,
            "message": "Password has been successfully updated",
            "auth_status": user.auth_status,
            "access": user.token()["access_token"],
            "refresh": user.token()["refresh_token"],
        })




