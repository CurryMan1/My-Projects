from PIL import Image, ImageTk


class BaseCounter(ImageTk.PhotoImage):
    def __init__(self, pos, img: str='Blank'):
        super.__init__(Image.open(f"assets/gfx/{img}.png").resize((100, 100)))

        self.pos = pos

    def move(self, x, y, repeat=False):

