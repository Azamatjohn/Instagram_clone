import random
import uuid
from datetime import timedelta, datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.regex_helper import normalize
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, identify_hasher

from shared.models import BaseModel

ORDINARY_USER, MANAGER, ADMIN = ('ordinary_user', 'manager', 'admin')
VIA_EMAIL, VIA_PHONE = ("via_email", "via_phone")
NEW, CODE_VERIFIED, DONE, PHOTO_STEP = ('new', 'code_verified', 'done', 'photo')

class User(AbstractUser, BaseModel):
    USER_ROLES = (
        (ORDINARY_USER, ORDINARY_USER),
        (MANAGER, MANAGER),
        (ADMIN,ADMIN)
    )
    AUTH_TYPE_CHOICES = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )
    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
        (PHOTO_STEP, PHOTO_STEP)
    )
    user_roles = models.CharField(max_length=31, default=ORDINARY_USER, choices=USER_ROLES)
    auth_type = models.CharField(max_length=31, choices=AUTH_TYPE_CHOICES, default=VIA_EMAIL )
    auth_status = models.CharField(max_length=31, default=NEW, choices=AUTH_STATUS)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=31, null=True, blank=True, unique=True)
    photo = models.ImageField(null=True, blank=True, upload_to='user_photos/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'heif']
                                                                   )]
                              )

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def create_verification_code(self, verify_type):
        code = str(random.randint(1000, 9999))
        UserConfirmation.objects.create(
            user_id=self.id,
            verify_type=verify_type,
            code=code,
        )
        return code

    def check_username(self):
        if not self.username:
            temp_username = f"instagram-{uuid.uuid4().__str__().split('-')[-1]}"
            while User.objects.filter(username=temp_username):
                temp_username = f"{temp_username}{random.randint(0, 9)}"
            self.username = temp_username

    def check_email(self):
        if self.email:
            normalize_email = self.email.lower()
            self.email = normalize_email

    # def check_password(self, password):
    #     if not self.password:
    #         temp_password = f"password-{uuid.uuid4().__str__().split('-')[-1]}"
    #         self.password = temp_password

    def hashing_password(self):
        # Only hash if it's NOT already hashed
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }



    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)

    def clean(self):
        self.check_username()
        self.check_email()
        self.hashing_password()


PHONE_EXPIRE = 2
EMAIL_EXPIRE = 5

class UserConfirmation(BaseModel):
    TYPE_CHOICES = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL),
    )
    code = models.CharField(max_length=4)
    verify_type = models.CharField(max_length=31, default=NEW, choices=TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verify_codes')
    expires_at = models.DateTimeField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())


    def save(self, *args, **kwargs):
        if self.verify_type == VIA_EMAIL:
            self.expires_at = datetime.now() + timedelta(minutes=EMAIL_EXPIRE)
        else:
            self.expires_at = datetime.now() + timedelta(minutes=PHONE_EXPIRE)
        super(UserConfirmation, self).save(*args, **kwargs)
