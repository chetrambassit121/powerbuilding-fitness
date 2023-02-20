from datetime import datetime

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    User,
)

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError("Users must have an email")
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(email=self.normalize_email(email), username=username,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email), username=username, password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class State(models.Model):  
    name = models.CharField(max_length=70, default=False)

    def __str__(self):
        return self.name


class City(models.Model):  
    state = models.ForeignKey(State, on_delete=models.CASCADE, default=False)
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=45, unique=True)
    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    password = models.CharField(max_length=100)
    date_joined = models.DateTimeField(verbose_name="date_joined", default=timezone.now)
    last_login = models.DateTimeField(verbose_name="last_login", default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = MyAccountManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        primary_key=True,
        verbose_name="user",
        related_name="profile",
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(
        upload_to="images/profile_pictures",
        default="images/default_pic.jpg",
        blank=False,
    )
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    followings = models.ManyToManyField(User, blank=True, related_name="followings")
    # following = models.ManyToManyField("self", blank=True, related_name="followers", symmetrical=False)
    website_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    # pinterest_url = models.CharField(max_length=255, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("home")

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class BroadCast_Email(models.Model):
    subject = models.CharField(max_length=200)
    created = models.DateTimeField(default=datetime.now)
    message = RichTextUploadingField(config_name="default")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "BroadCast Email to all Member"
        verbose_name_plural = "BroadCast Email"


