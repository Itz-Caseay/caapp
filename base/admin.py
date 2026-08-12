# ============================================
# ADMIN.PY
# ============================================

from django.contrib import admin
from .models import *

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'online_status', 'last_seen', 'created_at')
    list_filter = ('online_status', 'created_at')
    search_fields = ('user__username', 'user__fullname', 'phone_number')
    readonly_fields = ('last_seen', 'created_at', 'updated_at')
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Profile Info', {'fields': ('profile_pic', 'bio', 'phone_number')}),
        ('Status', {'fields': ('online_status', 'last_seen')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'group', 'content_preview', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp', 'sender')
    search_fields = ('sender__username', 'receiver__username', 'content')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    
    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_preview.short_description = 'Content'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'member_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'created_by__username', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'joined_at', 'is_admin')
    list_filter = ('is_admin', 'joined_at')
    search_fields = ('user__username', 'group__name')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact', 'is_favorite', 'created_at')
    list_filter = ('is_favorite', 'created_at')
    search_fields = ('user__username', 'contact__username', 'nickname')


# @admin.register(MessageAttachment)
# class MessageAttachmentAdmin(admin.ModelAdmin):
#     list_display = ('file_name', 'message', 'file_type', 'file_size', 'uploaded_at')
#     list_filter = ('file_type', 'uploaded_at')
#     search_fields = ('file_name', 'message__content')


# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ('recipient', 'title', 'notification_type', 'is_read', 'created_at')
#     list_filter = ('notification_type', 'is_read', 'created_at')
#     search_fields = ('recipient__username', 'title', 'message')


# @admin.register(TypingIndicator)
# class TypingIndicatorAdmin(admin.ModelAdmin):
#     list_display = ('user', 'receiver', 'group', 'is_typing', 'updated_at')
#     list_filter = ('is_typing', 'updated_at')
#     search_fields = ('user__username',)