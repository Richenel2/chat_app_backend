from channels.generic.websocket import AsyncJsonWebsocketConsumer

class MobileConsumer(AsyncJsonWebsocketConsumer):
    
        async def connect(self):
           await self.channel_layer.group_add("mobile",self.channel_name)
           await self.accept()
           await self.send_json({'message':"Mobile Connection successfull",'channelName':self.channel_name})


        async  def receive(self,text_data):
           await self.channel_layer.group_send(
               "mobile",
               {
                   "type":"message",
                   "body":{"message":"Un message"},
               },
           )      
    
        async def message(self,event):
          """ when you call a fonction"""
        #Send a message down to the client
          await self.send_json(event['body'])
        
  