from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from Learn_Box import settings
class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None, firstname=None, lastname=None, is_active=True
                    , is_staff=True, is_admin=True, is_student=False, is_instructor=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not firstname:
            raise ValueError("Users must have a first name")
        if not lastname:
            raise ValueError("Users must have a last name")
        user = self.model(
            email=self.normalize_email(email),
            # firstname=firstname,
            # lastname=lastname,
        )

        user.set_password(password)
        user.firstname = firstname
        user.lastname = lastname
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin
        user.is_student = is_student
        user.is_instructor = is_instructor
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
            is_active=True,
            is_staff=True,
        )
        return user

    def create_superuser(self, email, firstname, lastname, password):
        user = self.create_user(
            email,
            password=password,
            firstname=firstname,
            lastname=lastname,
            # is_staff=True,
            # is_admin=True,
            # is_superuser=True
        )
        return user


def get_profile_image_filename(instance, filename):
    return f"profile_images/{instance.pk}/profile_image_{filename}"


def get_default_profile_image():
    return 'img/default_profile_image.jpg'



class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', unique=True)
    firstname = models.CharField(max_length=40, blank=True, null=True)
    lastname = models.CharField(max_length=40, blank=True, null=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to=get_profile_image_filename, null=True, blank=True, default=get_default_profile_image)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']
    objects = MyAccountManager()


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
