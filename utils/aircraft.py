import math
import tkinter

from PIL import Image, ImageTk
from scipy.spatial.transform import Rotation

INTERVAL_RATE = 360


class Vector:
    def __init__(self, xyz=(0.0, 0.0, 0.0)):
        if isinstance(xyz, Vector):
            self.comps = xyz.comps
        else:
            self.comps = xyz

    def multiply(self, factor):
        return Vector([n * factor for n in self.comps])

    def add(self, vector):
        return Vector([n1 + n2 for (n1, n2) in zip(self.comps, vector.comps)])

    def magnitude(self):
        return math.sqrt(sum([x ** 2 for x in self.comps]))

    def square(self):
        return self.multiply(self.magnitude())

    def rotate(self, euler):
        return Vector(Rotation.from_euler('zxy', euler, degrees=True).apply(self.comps))

    def inverse_rotation(self, euler):
        return Vector(Rotation.from_euler('yxz', [-n for n in euler][::-1], degrees=True).apply(self.comps))

    def negate(self):
        return Vector([-n for n in self.comps])

    def dot(self, vector):
        return Vector([n1 * n2 for (n1, n2) in zip(self.comps, vector.comps)])


class TransformRB:
    def __init__(self, mass=1, drag_profiles=Vector((1, 1, 1)), position=Vector(), rotation=Vector(), gravity=-32,
                 position_d=Vector()):
        self.mass = mass
        self.drag_profiles = drag_profiles
        self.position = position
        self.rotation = rotation  # Roll, Pitch, Yaw
        self.gravity = gravity
        self.position_d = position_d

    def update(self, force=Vector(), relative_force=Vector(), wind_velocity=Vector(), rotation=Vector()):
        position_dd = force.multiply(1 / self.mass)
        position_dd = position_dd.add(Vector((0, self.gravity, 0)))
        interval = 1 / INTERVAL_RATE
        for i in range(int(6 * INTERVAL_RATE)):
            self.rotation = self.rotation.add(rotation.multiply(interval))
            a = position_dd.add(relative_force.rotate(self.rotation.comps).multiply(1 / self.mass))
            a_drag = self.position_d.add(wind_velocity.negate()).square().inverse_rotation(self.rotation.comps).dot(
                self.drag_profiles).rotate(self.rotation.comps).multiply(0.0765 / self.mass)
            a = a.add(a_drag.negate())
            print(f"a:{a.comps}")
            self.position = self.position.add(a.multiply(0.5 * (interval ** 2))).add(self.position_d.multiply(interval))
            self.position_d = self.position_d.add(a.multiply(interval))
            print(f"p:{self.position.comps}\npd:{self.position_d.comps}\npdd:{a.comps}\n")

    def to_string(self):
        return f"Position: {self.position.comps}\nPosition Prime: {self.position_d.comps}\nRotation: {self.rotation.comps}"


class Aircraft:
    def __init__(self, image, transform_rb=TransformRB()):
        self.transform_rb = transform_rb
        self.image = image

    def draw_on(self, canvas):
        img = self.image.rotate(-self.transform_rb.rotation.comps[2], Image.Resampling.BICUBIC, expand=True)
        canvas.paste(img, ([int(x) for x in self.transform_rb.position.add(Vector((img.width / -2, 0,
                                                                                   img.height / -2))).comps[::2]]), img)


def main():
    a = Aircraft(Image.open("airship_top.png"),
                 TransformRB(position=Vector((1200, 0, 1200)), rotation=Vector((0, 0, 45))))
    canvas = Image.open("airship_bg.png")
    a.draw_on(canvas)
    canvas.show()


def canvas_testing():
    top = tkinter.Tk()
    a = Aircraft(Image.open("airship_top.png"),
                 TransformRB(position=Vector((1200, 0, 1200)), rotation=Vector((0, 0, 45))))
    canvas = tkinter.Canvas(width=12000, height=12000, background="red", highlightthickness=0)
    bg = Image.open("airship_bg.png")
    bgi = ImageTk.PhotoImage(bg)
    canvas.create_image(0, 0, image=bgi, tag="testbg")
    a_comps = a.transform_rb.position.comps
    canvas.create_image(0, 0, image=ImageTk.PhotoImage(a.image), tag="testa")
    canvas.pack()
    top.mainloop()


def testing2():
    t = TransformRB(drag_profiles=Vector((4, 0.2, 15)), rotation=Vector((0, 80, 0)), mass=2,
                    position=Vector((0, 20000, 0)))
    print(f"{t.to_string()}\n")
    t.update(Vector((0, 0, 0)), rotation=Vector((360, 360, 360)), wind_velocity=Vector((0, 100, 0)))
    print(f"{t.to_string()}\n")


if __name__ == '__main__':
    testing2()
