#pylint:disable=E0001
import aiohttp
import re
from io import BytesIO
from json import loads
from typing import Tuple


from .exceptions import InvalidColor, SongNotFound, InvalidURL,\
                        SubRedditNotFound, ImageProcessFail,\
                        UserNotFound 
from .models import Color, Song, Thought, SubReddit,\
                    Quote, Asset, Car, GithubAccount
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
def urlcheck(url):
    if not URL_REGEX.match(url):
        raise InvalidURL(url)
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
            b=BytesIO(bytes).seek(0)
            
            return File(fp=b.read(),filename=name)
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

    async def sadcat(self,text):
        'https://api.popcat.xyz/sadcat?text=Your+Text' 
        async with self.get(apiurl("sadcat",text=text)) as resp:
            return self._process_image("sadcat.png",BytesIO(await resp.read()))
    
    async def oogway(self,text):
        "https://api.popcat.xyz/oogway?text=use+api.popcat.xyz"
        async with self.get(apiurl("oogway",text=text)) as resp:
            return self._process_image("oogway.png",BytesIO(await resp.read()))
            
    async def communism(self,url):
        """https://api.popcat.xyz/communism
        ?image=https://media.discordapp.net/
                  attachments/
                      819491776988839939/
                          876122609031471114/
                              colorify.png
        """
        if not URL_REGEX.match(url):
            raise InvalidURL(url)
        async with self.get(apiurl("communism",image=url)) as resp:
            if await error(resp):
                raise ValueError("Invalid image")
            return self._process_image("communism.png",BytesIO(await resp.read()))
    
    async def car(self):
        async with self.get(apiurl("car")) as resp:
            json=await resp.json()
            return Car(json["image"],json["title"])

    
    async def pooh(self,toptext,bottomtext):
        async with self.get(apiurl("pooh",text1=toptext,text2=bottomtext)) as resp:
            return self._process_image("pooh.png",BytesIO(await resp.read()))
    
    async def warning(self,image):
        "https://api.popcat.xyz/wanted?image=https://media.discordapp.net/attachments/819491776988839939/876122609031471114/colorify.png"
        urlcheck(image)
        async with self.get(apiurl("wanted",image=image)) as resp:
            if await error(resp):
                raise InvalidURL(image)
            return self._process_image("wanted.png",BytesIO(await resp.read()))
    async def github(self,user):
        async with self.get(apiurl("github/"+user)) as resp:
            if await error(resp):
                raise UserNotFound(user)
            return GithubAccount(payload=await resp.json())





