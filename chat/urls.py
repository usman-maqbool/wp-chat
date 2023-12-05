# chat/urls.py
from django.urls import path

from . import views
from chat.controller.views import *
urlpatterns = [
    path('create/chatrooms/', ChatRoomCreateView.as_view(), name='chatroom-create'),
    path('list/chatrooms/', ChatroomViewSet.as_view(), name='list-chatroom'),
    path('chatrooms/<int:pk>/leave/', LeaveChatroomView.as_view(), name='leave-chatroom'),
    path('chatrooms/<int:pk>/join/', JoinChatroomView.as_view(), name='join-chatroom'),
    path('chatrooms/<int:pk>/messages/', ChatroomMessagesView.as_view(), name='chatroom-messages'),
]