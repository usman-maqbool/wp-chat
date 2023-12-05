from chat.entity.models import Chatroom, Message

def create_chatroom(data):
    return Chatroom.objects.create(**data)

def get_all_chatrooms():
    return Chatroom.objects.all()

def get_messages_for_chatroom(chatroom_id):
    return Message.objects.filter(room_id=chatroom_id)

def leave_chatroom(user):
    return Chatroom.users.remove(user)

def join_chatroom(user):
    return Chatroom.users.add(user)