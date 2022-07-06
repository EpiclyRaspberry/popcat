from io import BytesIO

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
        self.img_url=img_url
    def __repr__(self):
        return f"<Color hex={self.hex} name={self.name} rgb={self.rgb} brightened={self.brightened} img_url={self.img_url}"

class Song(PopCatObject):
    def __init__(self,title, artist, image, lyrics):
        self.title=title
        self.artist=artist
        self.image=image
        self.lyrics=lyrics
    def __repr__(self):
        return ("<Song title={} artist={} image={} lyrics={}...".format(self.title,self.artist,self.image,self.lyrics[:20]))
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
        self.icon,self.banner=obj["icon"],obj["banner"]
        self.allowed_images,self.allowed_videos=obj["allow_images"],obj["allow_videos"]
        self.nsfw=obj["over_18"]
        self.url=obj["url"]



