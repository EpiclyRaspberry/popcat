from io import BytesIO

class Color:
    def __init__(self,hex,name,rgb, brightened,colorimg):
        self.hex=hex 
        self.name=name 
        self.rgb=rgb 
        self.brightened=brightened
        _img=BytesIO(colorimg)
        _img.seek(0)
        self.colorimg=_img
    def __repr__(self):
        return f"<Color hex={self.hex} name={self.name} rgb={self.rgb} brightened={self.brightened} colorimg={self.colorimg}"


