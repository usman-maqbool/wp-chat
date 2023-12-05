import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token
from   chat.entity.models import   Chatroom, Message, Attachment
from django.core.files.base import ContentFile


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        try:
            token_key = self.scope['query_string'].decode('utf-8').split('=')[1]
            token = Token.objects.get(key=token_key)
            self.user = token.user
        except Token.DoesNotExist:
            self.close()
        except token.user.DoesNotExist:
            self.close()
 
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        json_data = json.loads(text_data)
        message_content = json_data.get('message', None)
        file_data = json_data.get('file', None)

        if message_content and file_data:
            try:
                room = Chatroom.objects.get(name=self.room_name)

                message = Message.objects.create(room=room, user=self.user, content=message_content)
                attachment = Attachment.objects.create(message=message)
                attachment.file.save(file_data['filename'], ContentFile(file_data['content']))
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message_content,
                        'file': file_data
                    }
                )

            except Chatroom.DoesNotExist:
                raise Exception("Chatroom does not exist")

    def chat_message(self, event):
        message = event['message']
        file_data = event.get('file', None)
        self.send(text_data=json.dumps({
            'message': message,
            'file': file_data
        }))
