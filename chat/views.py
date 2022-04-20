from email import message
from rest_framework import viewsets
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from channels.layers import get_channel_layer
from rest_framework.response import Response
from asgiref.sync import async_to_sync

channel_layer=get_channel_layer()

from .serializers import UserSerializer,MessageSerializer
from .models import User,Message



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('creation_date')
    serializer_class = MessageSerializer

class PostMessage(APIView):
    def post(self, request):
        data = request.data
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            list = map( lambda x: MessageSerializer(x).data,Message.objects.all().order_by('creation_date')[:20])
            async_to_sync(channel_layer.group_send)("mobile",{"type":"message","body":list})
        else :
            raise ValidationError({'message':'No valid data '})
        return Response(data)

        
class Login(APIView):
    def post(self,request):

        reqBody = request.data
        email = reqBody['email']
        password = reqBody['password']
        try:

            user = User.objects.get(email=email)
        except BaseException as e:
            raise ValidationError({"message": f'{str(e)}'})
        if  not user.check_password(password):
            raise ValidationError({"message": "Incorrect Login credentials"})

        if user:
            if user.is_active:
                seriliazer = UserSerializer(user)

                Res =seriliazer.data

                return Response(Res)

            else:
                raise ValidationError({"message": f'user not active'})

        else:
            raise ValidationError({"message": f'user doesnt exist'})