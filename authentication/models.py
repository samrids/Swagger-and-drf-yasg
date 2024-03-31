# Create your models here.
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {'facebook': 'facebook', 
                  'google': 'google',
                  'twitter': 'twitter', 
                  'email': 'email'}


def get_organization_from_request(request):
    """Helper for backward compatibility with org_pk in session"""
    # TODO remove session logic in next release
    user = request.user
    if user and user.is_authenticated:
        if user.active_organization is None:
            organization_pk = request.session.get('organization_pk')
            if organization_pk:
                user.active_organization_id = organization_pk
                user.save()
                request.session.pop('organization_pk', None)
                request.session.modified = True
        return user.active_organization_id
        
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=150, null=True,blank=True)
    last_name = models.CharField(max_length=150, null=True,blank=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    nick_name = models.CharField(max_length=50, null=True,blank=True)
    bio = models.CharField(max_length=250,null=True,blank=True, default="Hey! I'm new here.")
    mobile = models.CharField(max_length=10,null=True,blank=True)
    facebook = models.CharField(max_length=255,null=True,blank=True)
    instagram = models.CharField(max_length=255,null=True,blank=True)
    youtube = models.CharField(max_length=255,null=True,blank=True)
    
    profile = models.ImageField(upload_to='profile-images/%y/%m/%d/', default='profile-images/default/memerrank-no-dp.jpg', blank=False, null=False)

    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    active_organization = models.ForeignKey(
        'organizations.Organization', null=True, on_delete=models.SET_NULL, related_name='active_users'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
