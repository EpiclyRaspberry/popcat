import aiohttp
from .exceptions import InvalidColor, SongNotFound
from .models import Color, Song

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
    




