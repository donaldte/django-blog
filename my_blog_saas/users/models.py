import uuid
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from django_extensions.db.models import TimeStampedModel, ActivatorModel


from .managers import UserManager




class AbstractBaseModel(TimeStampedModel, ActivatorModel):
    """
    Abstract base model that includes common fields for all models.
    All other models should inherit from this.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)  # Soft delete feature
    metadata = models.JSONField(default=dict, blank=True, null=True)
    

    class Meta:
        abstract = True  # This model won’t create a separate table

    def delete(self, *args, **kwargs):
        """
        Soft delete: Set is_active to False instead of deleting.
        """
        self.is_active = False
        self.save()

    def hard_delete(self, *args, **kwargs):
        """
        Permanently delete the instance from the database.
        """
        super().delete(*args, **kwargs)

    def restore(self, *args, **kwargs):
        """
        Restore a soft-deleted instance by setting is_active to True.
        """
        self.is_active = True
        self.save()


class User(AbstractUser):
    """
    Default custom user model for my_blog_saas.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
    
    
    def get_full_name(self) -> str:
        """Return the user's full name.

        Returns:
            str: The user's full name.

        """
        return self.name
    
    
    def get_location(self) -> str:
        """Return the user's location.

        Returns:
            str: The user's location.

        """
        return self.profile.location
    
    
    def get_website(self) -> str:
        """Return the user's website.

        Returns:
            str: The user's website.

        """
        return self.profile.website
    
    
    def get_bio(self) -> str:
        
        return self.profile.bio



class Profile(AbstractBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following", blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"