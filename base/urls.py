from django.urls import path
from .views import *

urlpatterns = [
    path('', login_user, name="login"),
    path('index/', index, name="index"),
    path('signup/', signup, name="signup"),
    path('logout/', logout_user, name="logout"),
    path('messages/', messages_view, name="messages"),
    path('messages/', messages_view, name='messages'),
    path('chat/<int:user_id>/', chat_detail_view, name='chat_detail'),
    path('send-message/', send_message_ajax, name='send_message'),
    path('get-new-messages/', get_new_messages, name='get_new_messages'),
    path('mark-read/<int:message_id>/', mark_message_read, name='mark_message_read'),
    path('mark-all-read/<int:user_id>/', mark_all_read, name='mark_all_read'),
    path('contacts/', contacts_view, name='contacts'),
    path('settings/', settings_view, name='settings'),
    path('groups/api/list/', get_user_groups_api, name="get_user_groups_api"),
    path('groups/create/', create_group_view, name='create_group'),
    path('groups/', groups_view, name='groups'),
    
    path('contacts/add/', add_contact_view, name='add_contact'),
    path('contacts/remove/<int:contact_id>/', remove_contact_view, name='remove_contact'),
    path('contacts/favorite/<int:contact_id>/', toggle_favorite_view, name='toggle_favorite'),
    path('groups/create/', create_group_view, name='create_group'),
    path('groups/<int:group_id>/', group_detail_view, name='group_detail'),
    path('groups/<int:group_id>/add-member/', add_group_member, name='add_group_member'),
    path('groups/<int:group_id>/leave/', leave_group, name='leave_group'),
    path('groups/<int:group_id>/transfer-admin/<int:user_id>/', transfer_admin, name='transfer_admin'),
    path('settings/update-status/', update_status_view, name='update_status'),
    path('send-voice-message/', send_voice_message_ajax, name='send_voice_message'),
]
