from rest_framework import serializers
from chat.entity.models import Chatroom, Message, Attachment




class MessageSerializer(serializers.ModelSerializer):
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["room","user","content","timestamp", "attachments"]

    def get_attachments(self, instance):
        attachments = instance.attachments.all() 
        serializer = AttachmentSerializer(attachments, many=True)
        return serializer.data


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['file', ]



class ChatroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'users']

