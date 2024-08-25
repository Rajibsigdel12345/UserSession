from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db import models

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username:str, email:str, first_name:str, last_name:str, password:str |None =None) -> 'User':
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username:str, email :str, first_name :str, last_name :str, password:str)-> 'User':
        user = self.create_user(
            username,
            email,
            first_name,
            last_name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    profile_url = models.URLField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    provider = models.CharField(max_length=100, default='local',choices=(('local','Local'),('google','Google'),('facebook','Facebook'),('twitter','Twitter'),('github','Github'),('linkedin','Linkedin')))

    def has_module_perms(self, app_label) ->bool:
        return self.is_superuser

    def has_perm(self, perm, obj=None)-> bool:
        return self.is_superuser


class AuthToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs) -> None:
        if not self.expires_at:
            self.expires_at = timezone.now()+settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.token}"

    