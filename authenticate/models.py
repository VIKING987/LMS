from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Email is Required!!")
        if not username:
            raise ValueError('Username is Required!!')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user=self.create_user(
            email=self.normalize_email(email), 
            username=username, 
            password=password)
        
        user.is_active=True
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True

        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    dues = models.FloatField(default=0)
    issue_limit = models.IntegerField(default=5)
    books_issued_curr = models.IntegerField(default=0)
    password = models.CharField(max_length=100)
    designation = models.CharField(max_length=10)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True