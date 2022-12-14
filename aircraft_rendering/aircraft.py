from PIL import Image

from physics import TransformRB
from visuals import ActiveImage


class Aircraft:
    def __init__(self):
        self.transform_rb = TransformRB()
        self.top_image = ActiveImage("./db/images/airship_top.png")
        self.side_image = ActiveImage("./db/images/airship_side.png")


class PropABC:
    def __init__(self):
        self.percent = 0


class Thruster(PropABC):
    def __init__(self, vector):
        super().__init__()
        self.vector = vector


class Rotator(PropABC):
    def __init__(self, vector):
        super().__init__()
        self.vector = vector

class Aircraft:
    def __init__(self, length: int, top: Image.Image, side: Image.Image, transform_rb=TransformRB()):
        self.length = length
        self.top = top
        self.side = side
        self.transform_rb = transform_rb

    def draw_on(self, canvas: Canvas):
        img = self.top if canvas.is_top else self.side
        ship_length = self.length * canvas.ppf
        new_dimensions = (int(img.width * ship_length / img.height if canvas.is_top else ship_length),
                          int(ship_length if canvas.is_top else img.height * ship_length / img.width))
        img = img.resize(new_dimensions, Image.Resampling.BICUBIC)
        img = img.rotate((-1 if canvas.is_top else 1)*self.transform_rb.rotation.comps[2 if canvas.is_top else 1], Image.Resampling.BICUBIC,
                         expand=True)
        canvas.paste(im=img, box=[int(x) for x in numpy.add((-img.width / 2, img.height / 2), numpy.multiply(
            self.transform_rb.coords()[:None if canvas.is_top else 0:2 if canvas.is_top else -1],
            canvas.ppf))], mask=img)
