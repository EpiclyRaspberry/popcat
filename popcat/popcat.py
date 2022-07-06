import aiohttp
import re
from io import BytesIO
from .exceptions import InvalidColor, SongNotFound, InvalidURL
from .models import Color, Song
URL_REGEX=re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
BASE_URL="https://api.popcat.xyz/"
COLOR_INVALID={"error":"Not valid!"}
SONG_NOT_FOUND={"error":"Song not found!"}
def apiurl(path,**params):
    param:str="?"
    if params:
        for pn,pv in params.items():
            param=f"{param}{pn}={pv}&"
        param=param[:-1]
    return BASE_URL+path+param
            
class PopCat:
    def __init__(self,*, session:aiohttp.ClientSession=None):
        if not session:
            self.session=aiohttp.ClientSession()
        else:
            self.session=session
        self.get=self.session.get
    async def __aenter__(self):
        return self
    async def __aexit__(self,e1,e2,e3):
        return await self.close()
        
    async def close(self):
        if session := self.session:
            await session.close()
    #apis
    async def color(self,color:str):
        async with self.session.get(BASE_URL+"color/"+color) as resp:
            res=await resp.json()
            if res==COLOR_INVALID:
                raise InvalidColor(color)
            #async with self.session.get(res["color_image"]) as colorimg:                
            return Color(res["hex"],res["name"],res["rgb"],res["brightened"],res["color_image"])
    async def lyrics (self,song:str):
        async with self.session.get(apiurl("lyrics/",song=song)) as resp:
            res=await resp.json()
            if res==SONG_NOT_FOUND:
                raise SongNotFound(song)
            return Song(res["title"], res["artist"],res["image"],res["lyrics"])
    async def screenshot(self,url):
        if URL_REGEX.match(url):
            async with self.get(apiurl("screenshot/",url=url)) as res:
                buffer=BytesIO(await res.read())
                buffer.seek(0)
                return buffer
        raise InvalidURL(url)
    async def chatbot(self,message,owner=None,botname=None):
        async with self.get(apiurl("chatbot/",msg=message,owner=owner, botname=botname)) as resp:
            return (await resp.json())["response"]




