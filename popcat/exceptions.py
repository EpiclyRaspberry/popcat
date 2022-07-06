class PopCatException(BaseException):
    pass


class InvalidColor(PopCatException):
    def __init__(self,color):
        self.color=color
        super().__init__(f"Color {color} is invalid")

class SongNotFound(PopCatException):
    def __init__(self, song):
        self.song=song 
        super().__init__(f"Song {song} not found")



