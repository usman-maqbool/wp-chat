from chat.service.serializers import ChatroomSerializer, MessageSerializer
from rest_framework.response import Response
from chat.repository.queries import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from chat.entity.models import User
from rest_framework import generics



class ChatroomMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        chatroom_id = self.kwargs['pk']
        return get_messages_for_chatroom(chatroom_id=chatroom_id)



class LeaveChatroomView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, ]

    queryset = get_all_chatrooms()
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user 
        if user in instance.users.all():
            leave_chatroom(user)
            return Response({'message': 'Successfully left the chatroom.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'You are not a member of this chatroom.'}, status=status.HTTP_400_BAD_REQUEST)    


class ChatRoomCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]

    serializer_class = ChatroomSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_ids = serializer.validated_data.pop('users', [])
        users = User.objects.filter(username__in=user_ids)
        user_ids = list(users.values_list('id', flat=True))
        chatroom = create_chatroom(serializer.validated_data)
        chatroom.users.set(users)
        
        serializer.validated_data['users'] = user_ids
        
        return Response(ChatroomSerializer(chatroom).data)
    



class ChatroomViewSet(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]

    queryset = get_all_chatrooms()
    serializer_class = ChatroomSerializer




class JoinChatroomView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ]

    queryset = get_all_chatrooms()
    serializer_class = ChatroomSerializer

    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user  
        if user not in instance.members.all():
            join_chatroom(user)
            return Response({'message': 'Successfully joined the chatroom.'}, status=status.HTTP_200_OK)
        return Response({'message': 'You are already a member of this chatroom.'}, status=status.HTTP_400_BAD_REQUEST)