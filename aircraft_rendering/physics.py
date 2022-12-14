import math

from scipy.spatial.transform import Rotation

INTERVAL_RATE = 360


class Vector:
    def __init__(self, xyz=(0.0, 0.0, 0.0)):
        if isinstance(xyz, Vector):
            self.comps = xyz.comps
        else:
            self.comps = xyz

    def multiply(self, factor):
        self.comps = [n * factor for n in self.comps]
        return self

    def add(self, vector):
        self.comps = [n1 + n2 for (n1, n2) in zip(self.comps, vector.comps)]
        return self

    def magnitude(self):
        return math.sqrt(sum([x ** 2 for x in self.comps]))

    def square(self):
        self.multiply(self.magnitude())
        return self

    def rotate(self, euler):
        self.comps = Rotation.from_euler('xzy', euler.comps, degrees=True).apply(self.comps)  # zxy
        return self

    def inverse_rotation(self, euler):
        self.comps = Rotation.from_euler('yzx', [-n for n in euler.comps][::-1], degrees=True).apply(self.comps)
        return self

    def negate(self):
        return self.multiply(-1)

    def dot(self, v):
        self.comps = [n1 * n2 for (n1, n2) in zip(self.comps, v.comps)]
        return self


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
        force.multiply(1 / self.mass).add(Vector((0, self.gravity, 0)))
        relative_force.multiply(1 / self.mass)
        interval = 1 / INTERVAL_RATE
        for i in range(int(INTERVAL_RATE)):
            self.rotation.add(Vector(rotation).multiply(interval))
            a_drag = Vector(self.position_d).add(Vector(wind_velocity).negate()).square().inverse_rotation(
                self.rotation).dot(self.drag_profiles).rotate(self.rotation).multiply(0.0765 / self.mass)
            a = Vector(force).add(Vector(relative_force).rotate(self.rotation)).add(a_drag.negate())
            self.position.add(Vector(a).multiply(0.5 * (interval ** 2))).add(Vector(self.position_d).multiply(interval))
            self.position_d.add(Vector(a).multiply(interval))
            print(self.rotation.comps)


if __name__ == '__main__':
    z = 1
    y = 0
    x = 0
    v = Vector((x, y, z))
    pitch = -24.75
    yaw = 0
    roll = 0
    print(Vector(v).rotate(Vector((roll, pitch, yaw))).comps)

# Pitch: 22` Yaw: 42` Roll: 33`

# Unity x y z
# Miney z y x

# Unity -Pitch, Yaw, -Roll
# Miney Roll, Pitch, Yaw
