class InvalidColor(BaseException):
    def __init__(self,color):
        self.color=color
        super().__init__(f"Color {color} is invalid")