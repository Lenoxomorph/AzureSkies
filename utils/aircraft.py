from PIL import Image
from scipy.spatial.transform import Rotation


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


class TransformRB:
    def __init__(self, position=Vector(), rotation=Vector()):
        self.position = position
        self.position_d = Vector()
        self.rotation = rotation  # Pitch, Yaw, Roll

    def update(self, position_dd):
        position_dd = position_dd.add(Vector((0, -32.174, 0)))
        self.position = self.position.add(self.position_d.multiply(6).add(position_dd.multiply(18)))
        self.position_d = self.position_d.add(position_dd.multiply(6))

    def to_string(self):
        return f"Position: {self.position.comps}\nPosition Prime: {self.position_d.comps}\nRotation: {self.rotation.comps}"


class Aircraft:
    def __init__(self, image, transform_rb=TransformRB()):
        self.transform_rb = transform_rb
        self.image = image

    def draw_on(self, canvas):
        img = self.image.rotate(-self.transform_rb.rotation.comps[1], Image.BICUBIC, expand=True)
        canvas.paste(img, ([int(x) for x in self.transform_rb.position.add(Vector((img.width/-2, 0,
                                                                                   img.height/-2))).comps[::2]]), img)


def main():
    a = Aircraft(Image.open("airship_top.png"), TransformRB(Vector((400, 0, 400)), Vector((0, 45, 0))))
    canvas = Image.open("airship_bg.png")
    a.draw_on(canvas)
    canvas.show()



def testing():
    x = 54
    y = 12
    z = -124
    r = Rotation.from_euler('zxy', (z, x, y), degrees=True)  # Roll, Pitch, Yaw
    print(f"0.5 in X: {r.apply((0.5, 0, 0))}")
    print(f"0.5 in Y: {r.apply((0, 0.5, 0))}")
    print(f"2 in Z: {r.apply((0, 0, 2))}")
    print()
    print(f"0.5 in XY: {r.apply((0.5, 0.5, 0))}")


def testing2():
    t = TransformRB(Vector((1, 2, 3)))
    print(f"{t.to_string()}\n")
    t.update(Vector((0, 1, 0)))
    print(f"{t.to_string()}\n")
    t.update(Vector((0, 0, 0)))
    print(f"{t.to_string()}\n")


def testing3():
    p = 34
    pd = 4
    pdd = 2
    interval = 0.1
    for i in range(int(6 / interval)):
        a = pdd - pd ** 2
        p += (0.5 * a * (interval ** 2)) + (pd * interval)
        pd += (a * interval)
        print(f"p:{p}\npd:{pd}\npdd:{pdd}\n")


if __name__ == '__main__':
    main()
