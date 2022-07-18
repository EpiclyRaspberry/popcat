import aiohttp
import re
from io import BytesIO
from json import loads
from typing import Tuple


from .exceptions import InvalidColor, SongNotFound, InvalidURL,\
                        SubRedditNotFound, ImageProcessFail
from .models import Color, Song, Thought, SubReddit,\
                    Quote, Asset
from .constants import *
try:
    from discord import File
except ImportError:
    File=None
try:
    from PIL import Image
except ImportError:
    Image=None

URL_REGEX=re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

BASE_URL="https://api.popcat.xyz/"
# endpoints erorrs
# deprecated 
COLOR_INVALID={"error":"Not valid!"}
SONG_NOT_FOUND={"error":"Song not found!"}
SUBREDDIT_NOT_FOUND={
 "error": "Invalid subreddit!"
}
# better error check
async def error(resp: aiohttp.ClientResponse):
    try: return (await resp.json()).keys()[0]=="error"
    except: return False
modes=[DPY,DISCORDPY,DEFAULT,PILLOW]

def apiurl(path,**params):
    param:str="?"
    if params:
        for pn,pv in params.items():
            param=f"{param}{pn}={pv}&"
        param=param[:-1]
    return BASE_URL+path+param
            
class PopCat:
    def __init__(self,*, session:aiohttp.ClientSession=None,image_mode:str=DEFAULT):
        if not session:
            self.session=aiohttp.ClientSession()
        else:
            self.session=session
        self.get=self.session.get
        if not image_mode in modes:
            raise ImageProcessFail("Invalid image mode.")
        self.image_mode=DEFAULT
        if image_mode == DPY:
            if not File:
                raise ModuleNotFoundError("Please install discord.py to use DISCORDPY image mode.")
                
            self.image_mode=image_mode
        if image_mode == PILLOW:
            if not Image:
                raise ModuleNotFoundError("Please install PIL/pillow to use PILLOW image mode.")
            self.image_mode=image_mode
    async def __aenter__(self):
        return self
    async def __aexit__(self,e1,e2,e3):
        return await self.close()
        
    async def close(self):
        if session := self.session:
            await session.close()
    def _process_image(self,name,bytes):
        if self.image_mode==DEFAULT:
            return Asset(name,bytes)
        elif self.image_mode==DISCORDPY:
            return File(fp=BytesIO(bytes).seek(0),filename=name)
        elif self.image_mode==PILLOW:
          try:
            return Image.open(bytes.read())
          except FileNotFoundError as e:
            raise ValueError("Cannot process image") from e
        raise ValueError("Invalid image mode provided\nProbably the code was stupid")
    #apis
    async def color(self,color:str):
        async with self.session.get(BASE_URL+"color/"+color) as resp:
            res=await resp.json()
            if await error(resp):
                raise InvalidColor(color)
            #async with self.session.get(res["color_image"]) as colorimg:                
            return Color(res["hex"],res["name"],res["rgb"],res["brightened"],res["color_image"])
    async def lyrics (self,song:str):
        async with self.session.get(apiurl("lyrics/",song=song)) as resp:
            res=await resp.json()
            if await error(resp):
                raise SongNotFound(song)
            return Song(res["title"], res["artist"],res["image"],res["lyrics"])
    async def screenshot(self,url):
        if URL_REGEX.match(url):
            async with self.get(apiurl("screenshot/",url=url)) as res:
                buffer=BytesIO(await res.read())
                buffer.seek(0)
                return self._process_image("screenshot.png",buffer)
        raise InvalidURL(url)
    async def chatbot(self,message,owner=None,botname=None):
        async with self.get(apiurl("chatbot",msg=message,owner=owner, botname=botname)) as resp:
            return (await resp.json())["response"]
    
    
    async def showerthoughts(self):
        async with self.get(apiurl("showerthoughts")) as resp:
            res=await resp.json()
            return Thought(res["result"],res["author"],res["upvotes"])
    async def quote (self):
        async with self.get(apiurl("quote")) as resp:
            res=await resp.json()
            return Quote(res["quote"], res["upvotes"])
    async def subreddit(self, subreddit):
        async with self.get(apiurl("subreddit/"+subreddit)) as resp:
            
            if await error(resp):
                raise SubRedditNotFound(subreddit)
            return SubReddit(await resp.json())
    async def lulcat(self,text):
        async with self.get(apiurl("lulcat",text=text)) as resp:
            return (await resp.json())["text"]

    async def fact(self):
        async with self.get(apiurl("fact")) as resp:
            return (await resp.json())["fact"]

    async def mock(self,text):
        async with self.get(apiurl("mock",text=text)) as resp:
            return (await resp.json())["text"]
    
    async def joke(self):
        async with self.get(apiurl("joke")) as resp:
            return (await resp.json())["joke"]

    async def welcomecard(self,background,texts:Tuple[str,str,str],avatar):
        "Unstable function"
        #f not URL_REGEX.match(background) or URL_REGEX.match(avatar):
        #    raise InvalidURL("\b")
        async with self.get(apiurl("welcomecard/", background=background,text1=texts[0],text2=texts[1],text3=texts[2],avatar=avatar)) as res:
            return self._process_image("card.png",BytesIO(await res.read()))


