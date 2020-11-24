from django.db import models

# # Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _



class UserManager(BaseUserManager):

    """
    Manages and creates different types of users
    """
    use_in_migration = True

    # default user 
    def _create_user(self, email, password = None, is_admin = False, is_active = True , is_staff = False , **extra_fields):

        if not email: 
            raise ValueError('Please enter a valid email')
        if not password:
            raise ValueError('Please enter a password')

        user_obj = self.model(
            email = self.normalize_email(email),
            **extra_fields
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff       
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using = self._db)
        return user_obj


    def create_user(self, email, password, **extra_fields):
        user = self._create_user(
            email,
            password = password,
            **extra_fields
        )
        user.is_superuser = False
        user.save(using=self._db)
        return user

        #create super user 
        
    def create_superuser(self, email, password, first_name = None, last_name = None , **extra_fields):
        user = self._create_user(
            email,
            password = password,
            **extra_fields
        )    
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using = self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    user model
    """
    username = models.CharField(max_length=20, blank=True,unique=True,null=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20,blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    photo = models.ImageField(upload_to='profile_pics', blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name','email', 'password']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)             