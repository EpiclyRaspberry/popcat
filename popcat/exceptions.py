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


class InvalidURL(PopCatException):
    def __init__(self,url):
        self.url=url 
        super().__init__(f"URL {url} is invalid")

class SubRedditNotFound(PopCatException):
    def __init__(self, subreddit):
        self.subreddit=subreddit 
        super().__init__(f"Subreddit {subreddit} not found")

class ImageProcessFail(PopCatException):
    pass


