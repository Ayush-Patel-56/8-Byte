from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Profile, UserPhoto
from api.s3_utils import delete_from_s3
import logging

logger = logging.getLogger(__name__)

# --- 1. Profile Avatar Cleanup ---

@receiver(pre_save, sender=Profile)
def delete_old_avatar_on_change(sender, instance, **kwargs):
    """
    Deletes the old avatar file from S3 when a new one is uploaded.
    """
    if not instance.pk:
        return False

    try:
        old_profile = Profile.objects.get(pk=instance.pk)
    except Profile.DoesNotExist:
        return False

    # Check if avatar has changed
    if old_profile.avatar and old_profile.avatar != instance.avatar:
        logger.info(f"Signal: Avatar changed for {instance.user.username}. Deleting old file: {old_profile.avatar.name}")
        delete_from_s3(old_profile.avatar.name)

@receiver(post_delete, sender=Profile)
def delete_avatar_on_profile_delete(sender, instance, **kwargs):
    """
    Deletes the avatar file from S3 when a Profile is deleted.
    """
    if instance.avatar:
        logger.info(f"Signal: Profile deleted for {instance.user.username}. Deleting avatar: {instance.avatar.name}")
        delete_from_s3(instance.avatar.name)


# --- 2. UserPhoto (Gallery) Cleanup ---

@receiver(post_delete, sender=UserPhoto)
def delete_photo_on_gallery_delete(sender, instance, **kwargs):
    """
    Deletes the gallery image file from S3 when a UserPhoto is deleted.
    """
    if instance.image:
        logger.info(f"Signal: Gallery photo deleted. Deleting file: {instance.image.name}")
        delete_from_s3(instance.image.name)
