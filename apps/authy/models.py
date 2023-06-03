import uuid

from django.contrib.auth.models import (
    AbstractUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class BaseModel(models.Model):
    """Base class for all models."""

    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    created = models.DateTimeField(db_index=True, editable=False, default=timezone.now)
    updated = models.DateTimeField(db_index=True, default=timezone.now)

    def save(self, *args, **kwargs):
        """Ensure validations are run and updated/created preserved."""
        self.updated = timezone.now()
        self.full_clean(exclude=None)
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        """Define a default least recently used ordering."""

        abstract = True
        ordering = ("-updated", "-created")


class BaseManager(BaseUserManager):
    def create_superuser(
        self, email, username, first_name, last_name, password, **other_fields
    ):
        other_fields = {
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
        }

        return self.create_user(
            email, username, first_name, last_name, password, **other_fields
        )

    def create_user(
        self, email, username, first_name, last_name, password, **other_fields
    ):
        if not email:
            raise ValueError("You must provide an email address. :sweat_smile:")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser, BaseModel, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"
        CLIENT = "CLIENT", "Client"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    objects = BaseManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.role = self.base_role
        return super().save(*args, **kwargs)


class StaffManager(BaseManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STAFF)


class Staff(User):
    base_role = User.Role.STAFF
    staff = StaffManager()

    class Meta:
        proxy = True


class StaffProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.IntegerField(null=True, blank=True)


class ClientManager(BaseManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CLIENT)


class Client(User):
    base_role = User.Role.CLIENT
    client = ClientManager()

    class Meta:
        proxy = True


class ClientProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    client_id = models.IntegerField(null=True, blank=True)


# User Profile creation signals
@receiver(post_save, sender=Client)
@receiver(post_save, sender=Staff)
def create_user_profile(sender, instance, created, **kwargs):
    user_profile_map = {
        Staff: StaffProfile,
        Client: ClientProfile,
        # Add other user type included
    }

    if created:
        user_profile_map[sender].objects.create(user=instance)
