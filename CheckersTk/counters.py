from PIL import Image, ImageTk


class BaseCounter(ImageTk.PhotoImage):
    def __init__(self, pos, img: str='Blank'):
        super().__init__(Image.open(f"assets/gfx/{img}.png").resize((100, 100)))

        self.pos = pos


class Man(BaseCounter):
    def __init__(self, pos, img: str, direction=None):
        super().__init__(pos, img)

        self.direction = direction

    def move(self, x, y, direction=0):
        if direction is None:
            direc

