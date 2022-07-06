from io import BytesIO

class Color:
    def __init__(self,hex,name,rgb, brightened,img_url):
        self.hex=hex 
        self.name=name 
        self.rgb=rgb 
        self.brightened=brightened
        self.img_url=img_url
    def __repr__(self):
        return f"<Color hex={self.hex} name={self.name} rgb={self.rgb} brightened={self.brightened} img_url={self.img_url}"

class Song:
    def __init__(self,title, artist, image, lyrics):
        self.title=title
        self.artist=artist
        self.image=image
        self.lyrics=lyrics
    def __repr__(self):
        return ("<Song title={} artist={} image={} lyrics={}...".format(self.title,self.artist,self.image,self.lyrics[:20]))
