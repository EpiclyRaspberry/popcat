from io import BytesIO
from typing import Union
from requests import get
try:
    from discord import File
except ImportError:
    File=None
try:
    from PIL import Image
except ImportError:
    Image=None
class PopCatObject:
    def __repr__(self):
        items = ("%s=%r" % (k, v) for k, v in self.__dict__.items())
        return "<%s %s>" % (self.__class__.__name__, ' '.join(items))



class Color(PopCatObject):
    def __init__(self,hex,name,rgb, brightened,img_url):
        self.hex=hex 
        self.name=name 
        self.rgb=rgb 
        self.brightened=brightened
        self.image=Asset(hex+".png",img_url)
    def __repr__(self):
        return f"<Color hex={self.hex} name={self.name} rgb={self.rgb} brightened={self.brightened} image={self.image}>"

class Song(PopCatObject):
    def __init__(self,title, artist, image, lyrics):
        self.title=title
        self.artist=artist
        self.image=Asset("song_thumbnail.png",image)
        self.lyrics=lyrics
    def __repr__(self):
        return ("<Song title={} artist={} image={} lyrics={}...>".format(self.title,self.artist,self.image,self.lyrics[:20]))
class Thought(PopCatObject):
    def __init__(self, result, author, upvotes):
        self.result=result 
        self.author=author 
        self.upvotes=upvotes
class SubReddit(PopCatObject):
    def __init__(self,obj):
        
        self.name=obj["name"]
        self.title=obj["title"]
        self.active_users=obj["active_users"]
        self.members=obj["members"]
        self.description=obj["description"]
        self.icon,self.banner=Asset(self.name+'_icon.png',obj["icon"]),Asset(self.name+"_banner.png",obj["banner"])
        self.allowed_images,self.allowed_videos=obj["allow_images"],obj["allow_videos"]
        self.nsfw=obj["over_18"]
        self.url=obj["url"]

class Quote(PopCatObject):
    def __init__(self,content, upvotes):
        self.content=content 
        self.upvotes=upvotes

class Asset(PopCatObject):
    def __init__(self,name,content:Union[BytesIO,str]):
        self._name=name 
        _con:BytesIO 
        
        if isinstance(content,str):
            
            _con=BytesIO(get(content).content)
        else:
            _con=content
        self._=_con
        _con.seek(0)
        self._content=_con
    
    @property
    def name(self):
        return self._name
    
    
    
    def as_dpy_file(self):
        if not File: raise ModuleNotFoundError("Please install discord.py to use this function")
        return File(fp=self._content,filename=self._name)
    def as_pil_image(self):
        if not Image: raise ModuleNotFoundError("Please install PIL/pillow to use this function")
        return Image.open(self._)
    def save(self,name="",path=None):
        name=name or self._name
        path=path or name 
        with open(path,"wb") as f:
            f.write(self._content)
        
