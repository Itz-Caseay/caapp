# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.http import HttpResponse
# from .models import *
# from django.http import HttpResponse, JsonResponse
# from django.db.models import Q
# from django.views.decorators.http import require_POST
# from django.utils import timezone

# # Create your views here.

# @login_required(login_url='login')
# def index(request):
#     user = request.user
#     recent_messages = Message.objects.filter(
#         Q(sender=user) | Q(receiver=user)
#     ).order_by('-timestamp')[:10]
    
#     contacts_count = Contact.objects.filter(user=user).count()
#     groups_count = user.chat_groups.count()
#     unread_count = Message.objects.filter(receiver=user, is_read=False).count()
    
#     context = {
#         'recent_messages': recent_messages,
#         'contacts_count': contacts_count,
#         'groups_count': groups_count,
#         'unread_count': unread_count,
#     }
#     return render(request, 'Profile/dashboard.html', context)

# # Login logic
# def login_user(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, f"Welcome back, {username}!")
#             return redirect('index')
        
#         else:
#             messages.error(request, "Invalid username or password.")
    
#     return render(request, "auth/login.html")

# # Register logic
# def signup(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         fullname = request.POST.get('fullname')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         password2 = request.POST.get('password2')
        
#         if password == password2:
#             if User.objects.filter(username=username).exists():
#                 messages.error(request, "Username taken")
#                 return redirect('signup')
#             elif User.objects.filter(email=email).exists():
#                 messages.error(request, "Email taken")
#                 return redirect('signup')
            
#             else:
#                 user = User.objects.create_user(
#                     username=username,
#                     fullname=fullname,
#                     email=email,
#                     password=password
#                 )
#                 user.save()
#                 profile = UserProfile.objects.create(user=user)
#                 profile.save()
#                 login(request, user)
#                 messages.success(request, f"Dear {username}, You just successfully created an account")
#                 return redirect('index')
#         else:
#             messages.error(request, "Passwords are not alike")
        
#     return render(request, "auth/signup.html")

# # Logout logic
# def logout_user(request):
#     logout(request)
#     messages.success(request, "Successfully logged out")
#     return redirect('login')

# @login_required(login_url='login')
# def messages_view(request):
#     """Display all conversations"""
#     user = request.user
    
#     # Get all contacts with their last messages
#     contacts = Contact.objects.filter(user=user).select_related('contact')
    
#     conversations = []
#     for contact_rel in contacts:
#         contact = contact_rel.contact
#         # Get last message
#         last_msg = Message.objects.filter(
#             (Q(sender=user, receiver=contact) | Q(sender=contact, receiver=user))
#         ).order_by('-timestamp').first()
        
#         # Count unread messages
#         unread_count = Message.objects.filter(
#             sender=contact, receiver=user, is_read=False
#         ).count()
        
#         # Get contact's online status
#         contact_profile = UserProfile.objects.filter(user=contact).first()
        
#         conversations.append({
#             'contact': contact,
#             'last_message': last_msg,
#             'unread_count': unread_count,
#             'is_online': contact_profile.online_status if contact_profile else False,
#             'profile_pic': contact_profile.profile_pic if contact_profile else None,
#         })
    
#     # Sort by latest message
#     conversations.sort(
#         key=lambda x: x['last_message'].timestamp if x['last_message'] else timezone.datetime.min,
#         reverse=True
#     )
    
#     # Get group conversations
#     groups = user.chat_groups.all()
#     group_conversations = []
#     for group in groups:
#         last_msg = group.messages.order_by('-timestamp').first()
#         group_conversations.append({
#             'group': group,
#             'last_message': last_msg,
#             'member_count': group.members.count(),
#         })
    
#     context = {
#         'conversations': conversations,
#         'group_conversations': group_conversations,
#     }
#     return render(request, 'messages.html', context)

# # Message viewing logic
# @login_required(login_url='login')
# def messages_view(request):
#     user = request.user
#     contacts = Contact.objects.filter(user=user).select_related('contact')
    
#     conversations = []
#     for contact_rel in contacts:
#         contact = contact_rel.contact
#         last_msg = Message.objects.filter(
#             (Q(sender=user, receiver=contact) | Q(sender=contact, receiver=user))
#         ).order_by('-timestamp').first()
        
#         unread_count = Message.objects.filter(
#             sender=contact, receiver=user, is_read=False
#         ).count()
        
#         contact_profile = UserProfile.objects.filter(user=contact).first()
        
#         conversations.append({
#             'contact': contact,
#             'last_message': last_msg,
#             'unread_count': unread_count,
#             'is_online': contact_profile.online_status if contact_profile else False,
#             'profile_pic': contact_profile.profile_pic if contact_profile else None,
#         })
    
#     conversations.sort(
#         key=lambda x: x['last_message'].timestamp if x['last_message'] else timezone.datetime.min,
#         reverse=True
#     )
    
#     groups = user.chat_groups.all()
#     group_conversations = []
#     for group in groups:
#         last_msg = group.messages.order_by('-timestamp').first()
#         group_conversations.append({
#             'group': group,
#             'last_message': last_msg,
#             'member_count': group.members.count(),
#         })
    
#     context = {
#         'conversations': conversations,
#         'group_conversations': group_conversations,
#     }
#     return render(request, 'Chat/messages.html', context)

# @login_required(login_url='login')
# def chat_detail_view(request, user_id):
#     other_user = get_object_or_404(User, id=user_id)
#     user = request.user
    
#     Message.objects.filter(
#         sender=other_user,
#         receiver=user,
#         is_read=False
#     ).update(is_read=True, read_at=timezone.now())
    
#     messages_list = Message.objects.filter(
#         (Q(sender=user, receiver=other_user) | 
#          Q(sender=other_user, receiver=user))
#     ).order_by('timestamp')
    
#     if request.method == 'POST':
#         content = request.POST.get('content', '').strip()
#         if content:
#             Message.objects.create(
#                 sender=user,
#                 receiver=other_user,
#                 content=content
#             )
#             return redirect('chat_detail', user_id=user_id)
#         else:
#             messages.error(request, "Message cannot be empty.")
    
#     other_profile = UserProfile.objects.filter(user=other_user).first()
    
#     context = {
#         'other_user': other_user,
#         'other_profile': other_profile,
#         'messages': messages_list,
#     }
#     return render(request, 'chat_detail.html', context)

# @login_required(login_url='login')
# @require_POST
# def send_message_ajax(request):
#     receiver_id = request.POST.get('receiver_id')
#     group_id = request.POST.get('group_id')
#     content = request.POST.get('content', '').strip()
    
#     if not content:
#         return JsonResponse({'error': 'Message cannot be empty'}, status=400)
    
#     sender = request.user
    
#     if receiver_id:
#         receiver = get_object_or_404(User, id=receiver_id)
#         message = Message.objects.create(
#             sender=sender,
#             receiver=receiver,
#             content=content
#         )
        
#         return JsonResponse({
#             'id': message.id,
#             'content': message.content,
#             'timestamp': message.timestamp.strftime('%I:%M %p'),
#             'sender': sender.fullname or sender.username,
#             'type': 'direct'
#         })
    
#     elif group_id:
#         group = get_object_or_404(Group, id=group_id)
#         if not group.members.filter(id=sender.id).exists():
#             return JsonResponse({'error': 'Not a member of this group'}, status=403)
        
#         message = Message.objects.create(
#             sender=sender,
#             group=group,
#             content=content
#         )
        
#         return JsonResponse({
#             'id': message.id,
#             'content': message.content,
#             'timestamp': message.timestamp.strftime('%I:%M %p'),
#             'sender': sender.fullname or sender.username,
#             'type': 'group',
#             'group_name': group.name
#         })
    
#     return JsonResponse({'error': 'Invalid recipient'}, status=400)

# @login_required(login_url='login')
# def get_new_messages(request):
#     user = request.user
#     last_message_id = request.GET.get('last_id', 0)
    
#     new_messages = Message.objects.filter(
#         receiver=user,
#         is_read=False,
#         id__gt=last_message_id
#     ).order_by('timestamp')
    
#     messages_data = []
#     for msg in new_messages:
#         sender_profile = UserProfile.objects.filter(user=msg.sender).first()
#         messages_data.append({
#             'id': msg.id,
#             'sender': msg.sender.fullname or msg.sender.username,
#             'sender_id': msg.sender.id,
#             'content': msg.content,
#             'timestamp': msg.timestamp.strftime('%I:%M %p'),
#             'profile_pic': sender_profile.profile_pic.url if sender_profile and sender_profile.profile_pic else None,
#         })
    
#     return JsonResponse({'messages': messages_data})

# @login_required(login_url='login')
# def mark_message_read(request, message_id):
#     message = get_object_or_404(Message, id=message_id, receiver=request.user)
#     message.is_read = True
#     message.read_at = timezone.now()
#     message.save()
#     return JsonResponse({'success': True})

# @login_required(login_url='login')
# def mark_all_read(request, user_id):
#     other_user = get_object_or_404(User, id=user_id)
#     count = Message.objects.filter(
#         sender=other_user,
#         receiver=request.user,
#         is_read=False
#     ).update(is_read=True, read_at=timezone.now())
    
#     return JsonResponse({'success': True, 'count': count})

# # Contact views
# @login_required(login_url='login')
# def contacts_view(request):
#     """Display contacts or search for users"""
#     user = request.user
#     search_query = request.GET.get('q', '').strip()
    
#     contact_list = []
    
#     if search_query:
#         # Search across ALL users (except the current user)
#         users = User.objects.filter(
#             Q(username__icontains=search_query) | 
#             Q(fullname__icontains=search_query)
#         ).exclude(id=user.id)
        
#         for found_user in users:
#             # Check if this user is already a contact
#             is_contact = Contact.objects.filter(user=user, contact=found_user).exists()
            
#             # Get user's profile
#             profile = UserProfile.objects.filter(user=found_user).first()
            
#             contact_list.append({
#                 'contact': found_user,
#                 'profile_pic': profile.profile_pic.url if profile and profile.profile_pic else None,
#                 'is_online': profile.online_status if profile else False,
#                 'is_contact': is_contact,
#             })
#     else:
#         # Show only contacts
#         contacts = Contact.objects.filter(user=user).select_related('contact')
        
#         for contact_rel in contacts:
#             contact = contact_rel.contact
#             profile = UserProfile.objects.filter(user=contact).first()
#             contact_list.append({
#                 'contact': contact,
#                 'profile_pic': profile.profile_pic.url if profile and profile.profile_pic else None,
#                 'is_online': profile.online_status if profile else False,
#                 'is_contact': True,
#             })
    
#     context = {
#         'contacts': contact_list,
#         'search_query': search_query,
#     }
#     return render(request, 'contacts.html', context)

# @login_required(login_url='login')
# @require_POST
# def add_contact_view(request):
#     """Add a new contact"""
#     username = request.POST.get('username')
#     if not username:
#         messages.error(request, 'Username is required.')
#         return redirect('contacts')
    
#     try:
#         contact_user = User.objects.get(username=username)
#         if contact_user == request.user:
#             messages.error(request, 'You cannot add yourself as a contact.')
#             return redirect('contacts')
        
#         # Check if already a contact
#         contact, created = Contact.objects.get_or_create(
#             user=request.user,
#             contact=contact_user
#         )
        
#         if created:
#             messages.success(request, f'{contact_user.fullname} added to contacts!')
#         else:
#             messages.info(request, f'{contact_user.fullname} is already in your contacts.')
            
#     except User.DoesNotExist:
#         messages.error(request, f'User "{username}" not found.')
    
#     return redirect('contacts')


# @login_required(login_url='login')
# @require_POST
# def remove_contact_view(request, contact_id):
#     """Remove a contact"""
#     Contact.objects.filter(user=request.user, id=contact_id).delete()
#     messages.success(request, 'Contact removed.')
#     return redirect('contacts')


# @login_required(login_url='login')
# @require_POST
# def toggle_favorite_view(request, contact_id):
#     """Toggle favorite status for a contact"""
#     contact = get_object_or_404(Contact, user=request.user, id=contact_id)
#     contact.is_favorite = not contact.is_favorite
#     contact.save()
#     messages.success(request, f'{"Added to" if contact.is_favorite else "Removed from"} favorites.')
#     return redirect('contacts')

# # Group view
# @login_required(login_url='login')
# def groups_view(request):
#     """Display all groups"""
#     user = request.user
#     groups = user.chat_groups.all().prefetch_related('members')
    
#     group_list = []
#     for group in groups:
#         members = group.members.all()
#         members_count = members.count()
#         online_count = UserProfile.objects.filter(
#             user__in=members,
#             online_status=True
#         ).count()
        
#         group_list.append({
#             'group': group,
#             'members_count': members_count,
#             'online_count': online_count,
#         })
    
#     context = {
#         'groups': group_list,
#     }
#     return render(request, 'Group/group.html', context)


# @login_required(login_url='login')
# def create_group_view(request):
#     """Create a new group"""
#     user = request.user
    
#     if request.method == 'POST':
#         name = request.POST.get('name', '').strip()
#         description = request.POST.get('description', '').strip()
#         profile_pic = request.FILES.get('profile_pic')
#         member_ids = request.POST.getlist('members')
        
#         if not name:
#             messages.error(request, 'Group name is required.')
#             return redirect('create_group')
        
#         # Check if group name already exists for this user
#         if Group.objects.filter(name=name, created_by=user).exists():
#             messages.error(request, 'You already have a group with this name.')
#             return redirect('create_group')
        
#         # Create group
#         group = Group.objects.create(
#             name=name,
#             description=description,
#             profile_pic=profile_pic,
#             created_by=user
#         )
        
#         # Add creator as admin
#         GroupMembership.objects.create(
#             user=user,
#             group=group,
#             is_admin=True
#         )
        
#         # Add selected members
#         for member_id in member_ids:
#             try:
#                 member = User.objects.get(id=member_id)
#                 if member != user:  # Don't add creator again
#                     GroupMembership.objects.get_or_create(
#                         user=member,
#                         group=group,
#                         defaults={'is_admin': False}
#                     )
#             except User.DoesNotExist:
#                 pass
        
#         messages.success(request, f'Group "{group.name}" created successfully!')
#         return redirect('group_detail', group_id=group.id)
    
#     # GET request - show form
#     # Get user's contacts with their profile info
#     contacts = Contact.objects.filter(user=user).select_related('contact')
    
#     contact_list = []
#     for contact_rel in contacts:
#         contact = contact_rel.contact
#         profile = UserProfile.objects.filter(user=contact).first()
#         contact_list.append({
#             'contact': contact,
#             'profile_pic': profile.profile_pic.url if profile and profile.profile_pic else None,
#             'is_online': profile.online_status if profile else False,
#         })
    
#     context = {
#         'contacts': contact_list,
#     }
#     return render(request, 'Group/create_group.html', context)


# @login_required(login_url='login')
# def group_detail_view(request, group_id):
#     """View and send messages in a group"""
#     group = get_object_or_404(Group, id=group_id)
#     user = request.user
    
#     # Check membership
#     if not group.members.filter(id=user.id).exists():
#         messages.error(request, 'You are not a member of this group.')
#         return redirect('groups')
    
#     # Get group messages
#     messages_list = group.messages.all().order_by('timestamp')
#     members = group.members.all()
    
#     # Check if user is admin
#     is_admin = GroupMembership.objects.filter(
#         user=user, 
#         group=group, 
#         is_admin=True
#     ).exists()
    
#     # Handle message sending
#     if request.method == 'POST':
#         content = request.POST.get('content', '').strip()
#         if content:
#             message = Message.objects.create(
#                 sender=user,
#                 group=group,
#                 content=content
#             )
#             return redirect('group_detail', group_id=group.id)
#         else:
#             messages.error(request, "Message cannot be empty.")
    
#     context = {
#         'group': group,
#         'messages': messages_list,
#         'members': members,
#         'is_admin': is_admin,
#     }
#     return render(request, 'Group/group_detail.html', context)


# @login_required(login_url='login')
# @require_POST
# def add_group_member(request, group_id):
#     """Add a member to a group (admin only)"""
#     group = get_object_or_404(Group, id=group_id)
#     user = request.user
    
#     # Check if user is admin
#     membership = get_object_or_404(GroupMembership, user=user, group=group)
#     if not membership.is_admin:
#         messages.error(request, 'Only group admins can add members.')
#         return redirect('group_detail', group_id=group.id)
    
#     username = request.POST.get('username')
#     try:
#         new_member = User.objects.get(username=username)
#         if group.members.filter(id=new_member.id).exists():
#             messages.warning(request, f'{new_member.fullname} is already a member.')
#         else:
#             GroupMembership.objects.create(user=new_member, group=group)
#             messages.success(request, f'{new_member.fullname} added to the group!')
#     except User.DoesNotExist:
#         messages.error(request, f'User "{username}" not found.')
    
#     return redirect('group_detail', group_id=group.id)


# @login_required(login_url='login')
# @require_POST
# def leave_group(request, group_id):
#     """Leave a group"""
#     group = get_object_or_404(Group, id=group_id)
#     membership = GroupMembership.objects.filter(user=request.user, group=group)
    
#     if membership.exists():
#         membership_obj = membership.first()
        
#         # Check if user is the only admin
#         admin_count = GroupMembership.objects.filter(group=group, is_admin=True).count()
#         if membership_obj.is_admin and admin_count == 1:
#             messages.error(request, 'You are the only admin. Transfer admin role before leaving.')
#             return redirect('group_detail', group_id=group.id)
        
#         membership.delete()
#         messages.success(request, f'You left "{group.name}".')
        
#         # Delete group if empty
#         if group.members.count() == 0:
#             group.delete()
#             messages.info(request, 'Group was empty and has been deleted.')
#             return redirect('groups')
    
#     return redirect('groups')


# @login_required(login_url='login')
# @require_POST
# def transfer_admin(request, group_id, user_id):
#     """Transfer admin role to another member"""
#     group = get_object_or_404(Group, id=group_id)
#     user = request.user
#     new_admin = get_object_or_404(User, id=user_id)
    
#     # Check if current user is admin
#     current_membership = get_object_or_404(GroupMembership, user=user, group=group)
#     if not current_membership.is_admin:
#         messages.error(request, 'Only admins can transfer admin role.')
#         return redirect('group_detail', group_id=group.id)
    
#     # Check if new admin is a member
#     new_membership = get_object_or_404(GroupMembership, user=new_admin, group=group)
    
#     # Transfer admin
#     current_membership.is_admin = False
#     current_membership.save()
    
#     new_membership.is_admin = True
#     new_membership.save()
    
#     messages.success(request, f'Admin role transferred to {new_admin.fullname}.')
#     return redirect('group_detail', group_id=group.id)

# # Profile setting
# @login_required(login_url='login')
# def settings_view(request):
#     """User settings/profile page"""
#     user = request.user
#     profile, created = UserProfile.objects.get_or_create(user=user)
    
#     if request.method == 'POST':
#         action = request.POST.get('action')
        
#         if action == 'profile':
#             # Update user info
#             fullname = request.POST.get('fullname', '').strip()
#             email = request.POST.get('email', '').strip()
#             bio = request.POST.get('bio', '').strip()
#             phone_number = request.POST.get('phone_number', '').strip()
            
#             if fullname:
#                 user.fullname = fullname
#             if email:
#                 user.email = email
#             user.save()
            
#             # Update profile
#             profile.bio = bio
#             profile.phone_number = phone_number
#             profile.save()
            
#             messages.success(request, 'Profile updated successfully!')
            
#         elif action == 'password':
#             # Change password
#             current = request.POST.get('current_password')
#             new1 = request.POST.get('new_password1')
#             new2 = request.POST.get('new_password2')
            
#             if not user.check_password(current):
#                 messages.error(request, 'Current password is incorrect.')
#             elif new1 != new2:
#                 messages.error(request, 'New passwords do not match.')
#             elif len(new1) < 8:
#                 messages.error(request, 'Password must be at least 8 characters.')
#             else:
#                 user.set_password(new1)
#                 user.save()
#                 messages.success(request, 'Password changed successfully!')
#                 # Re-login the user
#                 login(request, user)
                
#         elif action == 'remove_pic':
#             # Remove profile picture
#             if profile.profile_pic:
#                 profile.profile_pic.delete()
#                 profile.profile_pic = None
#                 profile.save()
#                 messages.success(request, 'Profile picture removed.')
                
#         elif action == 'delete_account':
#             # Delete account (with confirmation handled in template)
#             user.delete()
#             messages.success(request, 'Account deleted successfully.')
#             return redirect('login')
        
#         return redirect('settings')
    
#     context = {
#         'user': user,
#         'profile': profile,
#     }
#     return render(request, 'Profile/setting.html', context)

# @login_required
# def get_user_groups_api(request):
#     """API endpoint to get user's groups for the modal"""
#     user = request.user
#     groups = user.chat_groups.all()
    
#     groups_data = []
#     for group in groups:
#         groups_data.append({
#             'id': group.id,
#             'name': group.name,
#             'member_count': group.members.count(),
#         })
    
#     return JsonResponse({'groups': groups_data})

# @login_required(login_url='login')
# @require_POST
# def update_status_view(request):
#     """Update user online status via AJAX"""
#     user = request.user
#     status = request.POST.get('status') == 'true'
    
#     profile, created = UserProfile.objects.get_or_create(user=user)
#     profile.online_status = status
#     profile.last_seen = timezone.now()
#     profile.save()
    
#     return JsonResponse({'success': True})

# ============================================
# VIEWS.PY - COMPLETE FIXED
# ============================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import *
import json
import base64
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
import uuid

# ============================================
# AUTHENTICATION VIEWS
# ============================================

@login_required(login_url='login')
def index(request):
    """Dashboard view with WhatsApp-style data"""
    user = request.user
    profile = UserProfile.objects.filter(user=user).first()
    
    # Get conversations (same as messages)
    contacts = Contact.objects.filter(user=user).select_related('contact')
    conversations = []
    for contact_rel in contacts:
        contact = contact_rel.contact
        last_msg = Message.objects.filter(
            (Q(sender=user, receiver=contact) | Q(sender=contact, receiver=user))
        ).order_by('-timestamp').first()
        unread_count = Message.objects.filter(
            sender=contact, receiver=user, is_read=False
        ).count()
        prof = UserProfile.objects.filter(user=contact).first()
        conversations.append({
            'contact': contact,
            'last_message': last_msg,
            'unread_count': unread_count,
            'is_online': prof.online_status if prof else False,
            'profile_pic': prof.profile_pic.url if prof and prof.profile_pic else None,
        })
    conversations.sort(
        key=lambda x: x['last_message'].timestamp if x['last_message'] else timezone.datetime.min,
        reverse=True
    )
    
    # Group conversations
    groups = user.chat_groups.all()
    group_conversations = []
    for group in groups:
        last_msg = group.messages.order_by('-timestamp').first()
        group_conversations.append({
            'group': group,
            'last_message': last_msg,
        })
    
    # Stats
    contacts_count = Contact.objects.filter(user=user).count()
    groups_count = user.chat_groups.count()
    unread_count = Message.objects.filter(
        (Q(receiver=user) | Q(group__members=user)) & Q(is_read=False)
    ).exclude(sender=user).count()
    
    context = {
        'conversations': conversations,
        'group_conversations': group_conversations,
        'contacts_count': contacts_count,
        'groups_count': groups_count,
        'unread_count': unread_count,
        'user': user,
        'profile': profile,
    }
    return render(request, 'dashboard.html', context)
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Update online status
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.online_status = True
            profile.last_seen = timezone.now()
            profile.save()
            
            messages.success(request, f"Welcome back, {user.fullname}!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "auth/login.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username taken")
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email taken")
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username,
                    fullname=fullname,
                    email=email,
                    password=password
                )
                messages.success(request, f"Dear {fullname}, you successfully created an account!")
                login(request, user)
                return redirect('index')
        else:
            messages.error(request, "Passwords don't match")
    
    return render(request, "auth/signup.html")

def logout_user(request):
    # Update online status before logout
    if request.user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.online_status = False
        profile.last_seen = timezone.now()
        profile.save()
    
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('login')


# ============================================
# MESSAGES VIEWS
# ============================================

@login_required(login_url='login')
def messages_view(request):
    """Display all conversations"""
    user = request.user
    
    # Get all contacts with their last messages
    contacts = Contact.objects.filter(user=user).select_related('contact')
    
    conversations = []
    for contact_rel in contacts:
        contact = contact_rel.contact
        # Get last message
        last_msg = Message.objects.filter(
            (Q(sender=user, receiver=contact) | Q(sender=contact, receiver=user))
        ).order_by('-timestamp').first()
        
        # Count unread messages
        unread_count = Message.objects.filter(
            sender=contact, receiver=user, is_read=False
        ).count()
        
        # Get contact's profile
        profile = UserProfile.objects.filter(user=contact).first()
        
        conversations.append({
            'contact': contact,
            'last_message': last_msg,
            'unread_count': unread_count,
            'is_online': profile.online_status if profile else False,
            'profile_pic': profile.profile_pic.url if profile and profile.profile_pic else None,
        })
    
    # Sort by latest message
    conversations.sort(
        key=lambda x: x['last_message'].timestamp if x['last_message'] else timezone.datetime.min,
        reverse=True
    )
    
    # Get group conversations
    groups = user.chat_groups.all()
    group_conversations = []
    for group in groups:
        last_msg = group.messages.order_by('-timestamp').first()
        group_conversations.append({
            'group': group,
            'last_message': last_msg,
        })
    
    context = {
        'conversations': conversations,
        'group_conversations': group_conversations,
        'user': user,
    }
    return render(request, 'messages.html', context)

@login_required(login_url='login')
def chat_detail_view(request, user_id):
    """View and send messages with a specific user"""
    other_user = get_object_or_404(User, id=user_id)
    user = request.user
    
    # Mark unread messages as read
    Message.objects.filter(
        sender=other_user,
        receiver=user,
        is_read=False
    ).update(is_read=True, read_at=timezone.now())
    
    # Get all messages between users
    messages_list = Message.objects.filter(
        (Q(sender=user, receiver=other_user) | 
         Q(sender=other_user, receiver=user))
    ).order_by('timestamp')
    
    # Handle message sending - FIXED
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            message = Message.objects.create(
                sender=user,
                receiver=other_user,
                content=content
            )
            # Return to same page with anchor to latest message
            return redirect('chat_detail', user_id=user_id)
        else:
            messages.error(request, "Message cannot be empty.")
    
    # Get other user's profile
    other_profile = UserProfile.objects.filter(user=other_user).first()
    
    context = {
        'other_user': other_user,
        'other_profile': other_profile,
        'messages': messages_list,
        'user': user,
    }
    return render(request, 'chat_detail.html', context)
@login_required(login_url='login')
@require_POST
def send_message_ajax(request):
    """AJAX endpoint for sending messages without page reload"""
    receiver_id = request.POST.get('receiver_id')
    group_id = request.POST.get('group_id')
    content = request.POST.get('content', '').strip()
    
    if not content:
        return JsonResponse({'error': 'Message cannot be empty'}, status=400)
    
    sender = request.user
    
    if receiver_id:
        # Direct message
        receiver = get_object_or_404(User, id=receiver_id)
        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content
        )
        
        return JsonResponse({
            'id': message.id,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%I:%M %p'),
            'sender': sender.fullname or sender.username,
            'sender_id': sender.id,
            'type': 'direct'
        })
    
    elif group_id:
        # Group message
        group = get_object_or_404(Group, id=group_id)
        if not group.members.filter(id=sender.id).exists():
            return JsonResponse({'error': 'Not a member of this group'}, status=403)
        
        message = Message.objects.create(
            sender=sender,
            group=group,
            content=content
        )
        
        return JsonResponse({
            'id': message.id,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%I:%M %p'),
            'sender': sender.fullname or sender.username,
            'sender_id': sender.id,
            'type': 'group',
            'group_name': group.name
        })
    
    return JsonResponse({'error': 'Invalid recipient'}, status=400)


@login_required(login_url='login')
def get_new_messages(request):
    """Poll for new messages including voice messages"""
    user = request.user
    last_message_id = request.GET.get('last_id', 0)
    
    try:
        last_message_id = int(last_message_id)
    except ValueError:
        last_message_id = 0
    
    # Get new direct messages
    new_direct_messages = Message.objects.filter(
        receiver=user,
        is_read=False,
        id__gt=last_message_id
    ).exclude(sender=user).order_by('timestamp')
    
    # Get new group messages
    user_groups = user.chat_groups.all()
    new_group_messages = Message.objects.filter(
        group__in=user_groups,
        id__gt=last_message_id
    ).exclude(sender=user).order_by('timestamp')
    
    all_messages = list(new_direct_messages) + list(new_group_messages)
    all_messages.sort(key=lambda x: x.timestamp)
    
    messages_data = []
    for msg in all_messages:
        sender_profile = UserProfile.objects.filter(user=msg.sender).first()
        
        if msg.message_type == 'voice':
            content_data = {
                'type': 'voice',
                'duration': msg.voice_duration,
                'file_url': msg.voice_file.url if msg.voice_file else None,
            }
        else:
            content_data = {
                'type': 'text',
                'content': msg.content,
            }
        
        messages_data.append({
            'id': msg.id,
            'sender': msg.sender.fullname or msg.sender.username,
            'sender_id': msg.sender.id,
            'content': content_data,
            'timestamp': msg.timestamp.strftime('%I:%M %p'),
            'profile_pic': sender_profile.profile_pic.url if sender_profile and sender_profile.profile_pic else None,
            'type': 'group' if msg.group else 'direct',
            'group_name': msg.group.name if msg.group else None,
            'group_id': msg.group.id if msg.group else None,
        })
    
    return JsonResponse({'messages': messages_data})

@login_required(login_url='login')
def mark_message_read(request, message_id):
    """Mark a single message as read"""
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_read = True
    message.read_at = timezone.now()
    message.save()
    return JsonResponse({'success': True})


@login_required(login_url='login')
def mark_all_read(request, user_id):
    """Mark all messages from a user as read"""
    other_user = get_object_or_404(User, id=user_id)
    count = Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True, read_at=timezone.now())
    
    return JsonResponse({'success': True, 'count': count})


@login_required(login_url='login')
@require_POST
def delete_message_view(request, message_id):
    """Delete a message (only the sender can delete)"""
    message = get_object_or_404(Message, id=message_id)
    
    # Only sender can delete
    if message.sender != request.user:
        return JsonResponse({'error': 'You can only delete your own messages.'}, status=403)
    
    message.delete()
    return JsonResponse({'success': True})


# ============================================
# CONTACTS VIEWS
# ============================================

@login_required(login_url='login')
def contacts_view(request):
    """Display contacts or search for users"""
    user = request.user
    search_query = request.GET.get('q', '').strip()
    
    contact_list = []
    
    if search_query:
        # Search across ALL users (except the current user)
        users = User.objects.filter(
            Q(username__icontains=search_query) | 
            Q(fullname__icontains=search_query)
        ).exclude(id=user.id)
        
        for found_user in users:
            # Check if this user is already a contact
            is_contact = Contact.objects.filter(user=user, contact=found_user).exists()
            
            # Get user's profile
            profile = UserProfile.objects.filter(user=found_user).first()
            
            contact_list.append({
                'contact': found_user,
                'profile_pic': profile.profile_pic.url if profile and profile.profile_pic else None,
                'is_online': profile.online_status if profile else False,
                'is_contact': is_contact,
            })
    else:
        # Show only contacts
        contacts = Contact.objects.filter(user=user).select_related('contact')
        
        for contact_rel in contacts:
            contact = contact_rel.contact
            profile = UserProfile.objects.filter(user=contact).first()
            contact_list.append({
                'contact': contact,
                'profile_pic': profile.profile_pic.url if profile and profile.profile_pic else None,
                'is_online': profile.online_status if profile else False,
                'is_contact': True,
            })
    
    context = {
        'contacts': contact_list,
        'search_query': search_query,
        'user': user,
    }
    return render(request, 'contacts.html', context)


@login_required(login_url='login')
@require_POST
def add_contact_view(request):
    """Add a new contact"""
    username = request.POST.get('username')
    if not username:
        messages.error(request, 'Username is required.')
        return redirect('contacts')
    
    try:
        contact_user = User.objects.get(username=username)
        if contact_user == request.user:
            messages.error(request, 'You cannot add yourself as a contact.')
            return redirect('contacts')
        
        # Check if already a contact
        contact, created = Contact.objects.get_or_create(
            user=request.user,
            contact=contact_user
        )
        
        if created:
            messages.success(request, f'{contact_user.fullname} added to contacts!')
        else:
            messages.info(request, f'{contact_user.fullname} is already in your contacts.')
            
    except User.DoesNotExist:
        messages.error(request, f'User "{username}" not found.')
    
    return redirect('contacts')


@login_required(login_url='login')
@require_POST
def remove_contact_view(request, contact_id):
    """Remove a contact"""
    Contact.objects.filter(user=request.user, id=contact_id).delete()
    messages.success(request, 'Contact removed.')
    return redirect('contacts')


@login_required(login_url='login')
@require_POST
def toggle_favorite_view(request, contact_id):
    """Toggle favorite status for a contact"""
    contact = get_object_or_404(Contact, user=request.user, id=contact_id)
    contact.is_favorite = not contact.is_favorite
    contact.save()
    messages.success(request, f'{"Added to" if contact.is_favorite else "Removed from"} favorites.')
    return redirect('contacts')


# ============================================
# GROUPS VIEWS
# ============================================

@login_required(login_url='login')
def groups_view(request):
    """Display all groups the user is a member of"""
    user = request.user
    groups = user.chat_groups.all().prefetch_related('members')
    
    group_list = []
    for group in groups:
        members = group.members.all()
        members_count = members.count()
        online_count = UserProfile.objects.filter(
            user__in=members,
            online_status=True
        ).count()
        
        group_list.append({
            'group': group,
            'members_count': members_count,
            'online_count': online_count,
        })
    
    context = {
        'groups': group_list,
        'user': user,
    }
    return render(request, 'groups.html', context)


@login_required(login_url='login')
def create_group_view(request):
    """Create a new group"""
    user = request.user
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        profile_pic = request.FILES.get('profile_pic')
        member_ids = request.POST.getlist('members')
        
        if not name:
            messages.error(request, 'Group name is required.')
            return redirect('create_group')
        
        # Create group
        group = Group.objects.create(
            name=name,
            description=description,
            profile_pic=profile_pic,
            created_by=user
        )
        
        # Add creator as admin
        GroupMembership.objects.create(
            user=user,
            group=group,
            is_admin=True
        )
        
        # Add selected members
        for member_id in member_ids:
            try:
                member = User.objects.get(id=member_id)
                if member != user:
                    GroupMembership.objects.get_or_create(
                        user=member,
                        group=group,
                        defaults={'is_admin': False}
                    )
            except User.DoesNotExist:
                pass
        
        messages.success(request, f'Group "{group.name}" created successfully!')
        return redirect('group_detail', group_id=group.id)
    
    # GET request - show form
    # Get user's contacts with their profile info
    contacts = Contact.objects.filter(user=user).select_related('contact')
    
    contact_list = []
    for contact_rel in contacts:
        contact = contact_rel.contact
        profile = UserProfile.objects.filter(user=contact).first()
        contact_list.append({
            'contact': contact,
            'profile_pic': profile.profile_pic.url if profile and profile.profile_pic else None,
            'is_online': profile.online_status if profile else False,
        })
    
    context = {
        'contacts': contact_list,
        'user': user,
    }
    return render(request, 'create_group.html', context)


@login_required(login_url='login')
def group_detail_view(request, group_id):
    """View and send messages in a group"""
    group = get_object_or_404(Group, id=group_id)
    user = request.user
    
    # Check membership
    if not group.members.filter(id=user.id).exists():
        messages.error(request, 'You are not a member of this group.')
        return redirect('groups')
    
    # Get group messages
    messages_list = group.messages.all().order_by('timestamp')
    members = group.members.all()
    
    # Check if user is admin
    is_admin = GroupMembership.objects.filter(
        user=user, 
        group=group, 
        is_admin=True
    ).exists()
    
    # Get friends (contacts) that are not already in the group
    contacts = Contact.objects.filter(user=user).select_related('contact')
    friends = []
    for contact_rel in contacts:
        contact = contact_rel.contact
        profile = UserProfile.objects.filter(user=contact).first()
        
        # Calculate initials
        initials = "U"
        if contact.fullname:
            parts = contact.fullname.split()
            if len(parts) >= 2:
                initials = f"{parts[0][0]}{parts[1][0]}".upper()
            else:
                initials = contact.fullname[:2].upper()
        elif contact.username:
            initials = contact.username[:2].upper()
        
        friends.append({
            'id': contact.id,
            'username': contact.username,
            'fullname': contact.fullname,
            'initials': initials,
            'profile_pic': profile.profile_pic.url if profile and profile.profile_pic else None,
            'is_online': profile.online_status if profile else False,
            'in_group': group.members.filter(id=contact.id).exists(),
        })
    
    # Handle message sending - FIXED
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            message = Message.objects.create(
                sender=user,
                group=group,
                content=content
            )
            return redirect('group_detail', group_id=group.id)
        else:
            messages.error(request, "Message cannot be empty.")
    
    context = {
        'group': group,
        'messages': messages_list,
        'members': members,
        'is_admin': is_admin,
        'friends': friends,
        'user': user,
    }
    return render(request, 'group_detail.html', context)

@login_required(login_url='login')
@require_POST
def add_group_member(request, group_id):
    """Add a member to a group (admin only)"""
    group = get_object_or_404(Group, id=group_id)
    user = request.user
    
    # Check if user is admin
    membership = get_object_or_404(GroupMembership, user=user, group=group)
    if not membership.is_admin:
        return JsonResponse({'success': False, 'error': 'Only group admins can add members.'}, status=403)
    
    # Get user_id from JSON or form data
    try:
        import json
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            user_id = data.get('user_id')
        else:
            user_id = request.POST.get('user_id')
    except:
        user_id = request.POST.get('user_id')
    
    if not user_id:
        return JsonResponse({'success': False, 'error': 'User ID required.'}, status=400)
    
    try:
        new_member = User.objects.get(id=user_id)
        if group.members.filter(id=new_member.id).exists():
            return JsonResponse({'success': False, 'error': 'Already a member.'}, status=400)
        else:
            GroupMembership.objects.create(user=new_member, group=group)
            return JsonResponse({'success': True, 'message': f'{new_member.username} added to the group!'})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found.'}, status=404)


@login_required(login_url='login')
@require_POST
def leave_group(request, group_id):
    """Leave a group"""
    group = get_object_or_404(Group, id=group_id)
    membership = GroupMembership.objects.filter(user=request.user, group=group)
    
    if membership.exists():
        membership_obj = membership.first()
        
        # Check if user is the only admin
        admin_count = GroupMembership.objects.filter(group=group, is_admin=True).count()
        if membership_obj.is_admin and admin_count == 1:
            messages.error(request, 'You are the only admin. Transfer admin role before leaving.')
            return redirect('group_detail', group_id=group.id)
        
        membership.delete()
        messages.success(request, f'You left "{group.name}".')
        
        # Delete group if empty
        if group.members.count() == 0:
            group.delete()
            messages.info(request, 'Group was empty and has been deleted.')
            return redirect('groups')
    
    return redirect('groups')


@login_required(login_url='login')
@require_POST
def transfer_admin(request, group_id, user_id):
    """Transfer admin role to another member"""
    group = get_object_or_404(Group, id=group_id)
    user = request.user
    new_admin = get_object_or_404(User, id=user_id)
    
    # Check if current user is admin
    current_membership = get_object_or_404(GroupMembership, user=user, group=group)
    if not current_membership.is_admin:
        messages.error(request, 'Only admins can transfer admin role.')
        return redirect('group_detail', group_id=group.id)
    
    # Check if new admin is a member
    new_membership = get_object_or_404(GroupMembership, user=new_admin, group=group)
    
    # Transfer admin
    current_membership.is_admin = False
    current_membership.save()
    
    new_membership.is_admin = True
    new_membership.save()
    
    messages.success(request, f'Admin role transferred to {new_admin.fullname}.')
    return redirect('group_detail', group_id=group.id)


@login_required(login_url='login')
def get_user_groups_api(request):
    """API endpoint to get user's groups for the modal"""
    user = request.user
    groups = user.chat_groups.all()
    
    groups_data = []
    for group in groups:
        groups_data.append({
            'id': group.id,
            'name': group.name,
            'member_count': group.members.count(),
        })
    
    return JsonResponse({'groups': groups_data})


# ============================================
# PROFILE / SETTINGS VIEWS
# ============================================

@login_required(login_url='login')
def settings_view(request):
    """User settings/profile page"""
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'profile':
            # Update user info
            fullname = request.POST.get('fullname', '').strip()
            email = request.POST.get('email', '').strip()
            bio = request.POST.get('bio', '').strip()
            phone_number = request.POST.get('phone_number', '').strip()
            
            if fullname:
                user.fullname = fullname
            if email:
                user.email = email
            user.save()
            
            # Update profile
            profile.bio = bio
            profile.phone_number = phone_number
            profile.save()
            
            messages.success(request, 'Profile updated successfully!')
            
        elif action == 'password':
            # Change password
            current = request.POST.get('current_password')
            new1 = request.POST.get('new_password1')
            new2 = request.POST.get('new_password2')
            
            if not user.check_password(current):
                messages.error(request, 'Current password is incorrect.')
            elif new1 != new2:
                messages.error(request, 'New passwords do not match.')
            elif len(new1) < 8:
                messages.error(request, 'Password must be at least 8 characters.')
            else:
                user.set_password(new1)
                user.save()
                messages.success(request, 'Password changed successfully!')
                # Re-login the user
                login(request, user)
                
        elif action == 'remove_pic':
            # Remove profile picture
            if profile.profile_pic:
                profile.profile_pic.delete()
                profile.profile_pic = None
                profile.save()
                messages.success(request, 'Profile picture removed.')
                
        elif action == 'delete_account':
            # Delete account (with confirmation handled in template)
            user.delete()
            messages.success(request, 'Account deleted successfully.')
            return redirect('login')
        
        return redirect('settings')
    
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'settings.html', context)


@login_required(login_url='login')
@require_POST
def update_status_view(request):
    """Update user online status via AJAX"""
    user = request.user
    status = request.POST.get('status') == 'true'
    
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.online_status = status
    profile.last_seen = timezone.now()
    profile.save()
    
    return JsonResponse({'success': True})

import base64
import uuid
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

@login_required(login_url='login')
@require_POST
def send_voice_message_ajax(request):
    """AJAX endpoint for sending voice messages"""
    receiver_id = request.POST.get('receiver_id')
    group_id = request.POST.get('group_id')
    voice_data = request.POST.get('voice_data')  # base64 encoded audio
    voice_duration = request.POST.get('voice_duration')
    
    if not voice_data:
        return JsonResponse({'error': 'Voice data is required'}, status=400)
    
    # Decode base64 audio
    try:
        # Remove data URL prefix if present
        if 'base64,' in voice_data:
            voice_data = voice_data.split('base64,')[1]
        
        audio_bytes = base64.b64decode(voice_data)
        audio_file = ContentFile(audio_bytes)
        
        # Generate unique filename
        filename = f"voice_{uuid.uuid4().hex[:8]}.webm"
        
        # Save file
        file_path = default_storage.save(f'voice_messages/{filename}', audio_file)
        file_url = default_storage.url(file_path)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
    sender = request.user
    
    if receiver_id:
        receiver = get_object_or_404(User, id=receiver_id)
        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            message_type='voice',
            voice_file=file_path,
            voice_duration=int(voice_duration) if voice_duration else None
        )
        return JsonResponse({
            'id': message.id,
            'type': 'voice',
            'duration': message.voice_duration,
            'timestamp': message.timestamp.strftime('%I:%M %p'),
            'sender': sender.fullname or sender.username,
            'sender_id': sender.id,
            'file_url': file_url,
        })
    
    elif group_id:
        group = get_object_or_404(Group, id=group_id)
        if not group.members.filter(id=sender.id).exists():
            return JsonResponse({'error': 'Not a member of this group'}, status=403)
        
        message = Message.objects.create(
            sender=sender,
            group=group,
            message_type='voice',
            voice_file=file_path,
            voice_duration=int(voice_duration) if voice_duration else None
        )
        return JsonResponse({
            'id': message.id,
            'type': 'voice',
            'duration': message.voice_duration,
            'timestamp': message.timestamp.strftime('%I:%M %p'),
            'sender': sender.fullname or sender.username,
            'sender_id': sender.id,
            'file_url': file_url,
            'group_name': group.name
        })
    
    return JsonResponse({'error': 'Invalid recipient'}, status=400)
