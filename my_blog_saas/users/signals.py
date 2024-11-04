from my_blog_saas.users.models import User, Profile
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        