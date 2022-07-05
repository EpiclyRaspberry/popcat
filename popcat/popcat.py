import aiohttp
from .exceptions import  InvalidColor
from .models import Color

BASE_API="https://api.popcat.xyz/"
COLOR_INVALID={"error":"Not valid!"}
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
        async with self.session.get(BASE_API+"color/"+color) as resp:
            res=await resp.json()
            if res==COLOR_INVALID:
                raise InvalidColor(color)
            async with self.session.get(res["color_image"]) as colorimg:                
                
                return Color(res["hex"],res["name"],res["rgb"],res["brightened"], await colorimg.read())

            