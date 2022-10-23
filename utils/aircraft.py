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
        self.rotation = rotation

    def update(self, position_dd):
        position_dd = position_dd.add(Vector((0, -9.8, 0)))
        self.position = self.position.add(self.position_d.multiply(6).add(position_dd.multiply(18)))
        self.position_d = self.position_d.add(position_dd.multiply(6))

    def to_string(self):
        return f"Position: {self.position.comps}\nPosition Prime: {self.position_d.comps}\nRotation: {self.rotation.comps}"


class Aircraft:
    def __init__(self, image, transform_rb=TransformRB()):
        self.transform_rb = transform_rb
        self.image = image


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


if __name__ == '__main__':
    testing()
