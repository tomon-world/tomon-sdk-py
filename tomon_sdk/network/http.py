from . import route


class HTTPClient:
    def __init__(self):
        pass
    
    # send message
    async def send_message(self, token, channel_id, content, embed=None, nonce=None, forward=None, reply = None):
        
        try:
            payload = {}
            if content:
                payload['content'] = content

            if embed:
                payload['embed'] = embed

            if nonce:
                payload['nonce'] = nonce
                
            if reply:
                payload['reply'] = reply
                
            if forward:
                payload['forward'] = forward
                
            
            await route.Route(path='/channels/{}/messages'.format(channel_id), token=token).post(data=payload,auth = True)
        except Exception as e:
            print(e)
            
    # send files    
    async def send_files(self, token, channel_id, content, files, embed=None, nonce=None, forward=None, reply=None ):
        
        try:
            payload = {}
            if content:
                payload['content'] = content

            if embed:
                payload['embed'] = embed

            if nonce:
                payload['nonce'] = nonce
                
            if reply:
                payload['reply'] = reply
                
            if forward:
                payload['forward'] = forward
                
            
            await route.Route(path='/channels/{}/messages'.format(channel_id), token = token).post(data = payload, files = files, auth = True)
        except Exception as e:
            print(e)
            
    # edit message        
    async def edit_message(self, token, channel_id, message_id, content, embed=None, nonce=None, forward=None, reply=None  ):
        try:
            payload = {}
            if content:
                payload['content'] = content

            if embed:
                payload['embed'] = embed

            if nonce:
                payload['nonce'] = nonce
                
            if reply:
                payload['reply'] = reply
                
            if forward:
                payload['forward'] = forward
                
            await route.Route(path= '/channels/{}/messages/{}'.format(channel_id, message_id),token = token).patch(data = payload, auth = True) 
        except Exception as e:
            print(e)       
    
    # get guild channels
    async def get_guild_channels(self, token, guild_id):
    
        try:
            channels = await route.Route(path='/guilds/{}/channels'.format(guild_id), token=token).get( auth = True)
        except Exception as e:
            print(e)
        return channels 
    
    
