from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import Message
from .serializers import MessageSerializer
from asgiref.sync import sync_to_async

class MobileConsumer(AsyncJsonWebsocketConsumer):
    
        async def connect(self):
            await self.channel_layer.group_add("mobile",self.channel_name)
            await self.accept()
            list = sync_to_async(map( lambda x: MessageSerializer(x).data,Message.objects.all().order_by('creation_date')[:20]))
            await self.send_json(list)


        async  def receive(self,text_data):
           await self.channel_layer.group_send(
               "mobile",
               {
                   "type":"message",
                   "body":{"message":"Un message"},
               },
           )      
    
        async def message(self,event):
          list = sync_to_async(map( lambda x: MessageSerializer(x).data,Message.objects.all().order_by('creation_date')[:20]))
          await self.send_json(list)
        
  