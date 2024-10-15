from django.db import models, IntegrityError
from django.core.files.storage import default_storage
from django.contrib.postgres import fields
from django.contrib.postgres.fields import ArrayField
import json
from django import forms
import uuid
from django.contrib.auth.models import Permission, Group, User, ContentType
from django.contrib.auth import login
from django.db.models.signals import post_save
from django.dispatch import receiver

# When a new User is saved...
@receiver(post_save, sender=User)
def create_user_group(sender, instance, created, **kwargs):
    # If the User was just created...
    if created:
        # Create a new Group with the same name as the username
        group, created = Group.objects.get_or_create(name=instance.username)
        if created:
            # Get the content type for the User model
            content_type = ContentType.objects.get_for_model(instance)
            # Get all permissions for the User model
            permissions = Permission.objects.filter(content_type=content_type)
            # Assign the permissions to the Group
            group.permissions.set(permissions)

# When a User is saved...
@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, **kwargs):
    # Get the Group with the same name as the username
    group = Group.objects.get(name=instance.username)
    # Add the User to the Group
    instance.groups.add(group)

#binder
class Binder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user.widget = forms.HiddenInput()
    user.editable = False
    class Meta:
        permissions = [
            ("view_mymodel", "Can view my model"),
        ]

def get_default_user():
    try:
        return User.objects.get(username='current_user')
    except User.DoesNotExist:
        return User.objects.create(username='current_user')

#folder
class Folder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    userList = models.JSONField(default=list, blank=True, null=True) # list of users who have access to the folder
    userSignCount = models.JSONField(default=list, blank=True, null=True) # list of users who have signed the folder
    userActive = models.JSONField(default=list, blank=True, null=True) # most active user in the folder
    privledgeActiveUser = models.JSONField(default=list, blank=True, null=True) # privledge of the most active user
    ipWhois = models.JSONField(default=list, blank=True, null=True) # includes geo lcoations for ip address and other metadata
    userLocation = models.JSONField(default=list, blank=True, null=True) # location of the most active user
    userMap = models.FileField(upload_to='./order365/static/maps/', blank=True)
    threatIp = models.JSONField(default=dict, blank=True, null=True)
    binderId = models.ForeignKey(Binder, related_name='folders', on_delete=models.CASCADE)
    class Meta:
        permissions = [
            ("view_mymodel", "Can view my model"),
        ]
#file 
class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    userList = models.JSONField(default=list, blank=True, null=True) # list of users who have access to the folder
    userSignCount = models.JSONField(default=list, blank=True, null=True) # list of users who have signed the folder
    userActive = models.JSONField(default=list, blank=True, null=True) # most active user in the folder
    privledgeActiveUser = models.JSONField(default=list, blank=True, null=True) # privledge of the most active user
    ipWhois = models.JSONField(default=list, blank=True, null=True) # includes geo lcoations for ip address and other metadata
    userLocation = models.JSONField(default=list, blank=True, null=True) # location of the most active user
    userMap = models.FileField(upload_to='./order365/static/maps/', blank=True)
    threatIp = models.JSONField(default=dict, blank=True, null=True)
    file = models.FileField(upload_to='./order365/static/uploads/', blank=True)
    dataDoct = models.JSONField(default=list, blank=True, null=True)
    folderId = models.ForeignKey(Folder, related_name='files', on_delete=models.CASCADE)
    
class Configurations(models.Model):
     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     badIp = fields.ArrayField(models.CharField(max_length=15), default=list)
     badCidr =  fields.ArrayField(models.CharField(max_length=20), default=list)
     badDomain = fields.ArrayField(models.CharField(max_length=256), default=list)
     ipIngestion = fields.ArrayField(models.URLField(max_length=256), default=list)
     domainIngestion = fields.ArrayField(models.URLField(max_length=256), default=list)
