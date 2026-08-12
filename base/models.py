from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random
import string
import uuid

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, blank=False)
    fullname = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=254, unique=True, blank=False)
    
    def __str__(self):
        return f"{self.username} joined"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    online_status = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
class Message(models.Model):
    """Chat message model with voice support"""
    MESSAGE_TYPES = (
        ('text', 'Text'),
        ('voice', 'Voice'),
        ('image', 'Image'),
        ('file', 'File'),
    )
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='received_messages')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, blank=True, related_name='messages')
    content = models.TextField(blank=True, null=True)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    voice_file = models.FileField(upload_to='voice_messages/', null=True, blank=True)
    voice_duration = models.IntegerField(null=True, blank=True, help_text="Duration in seconds")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['sender', 'receiver', 'timestamp']),
            models.Index(fields=['group', 'timestamp']),
            models.Index(fields=['receiver', 'is_read']),
        ]

    def __str__(self):
        if self.message_type == 'voice':
            return f"{self.sender.username}: 🎤 Voice message ({self.voice_duration}s)"
        return f"{self.sender.username}: {self.content[:30]}"

class Group(models.Model):
    name = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='group_pics/', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_groups'
    )
    members = models.ManyToManyField(
        User, 
        related_name='chat_groups',
        through='GroupMembership'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class GroupMembership(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='group_memberships'
    )
    group = models.ForeignKey(
        Group, 
        on_delete=models.CASCADE, 
        related_name='memberships'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'group']

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"

class Contact(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='contacts'
    )
    contact = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='contacted_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'contact']

    def __str__(self):
        return f"{self.user.username} - {self.contact.username}"