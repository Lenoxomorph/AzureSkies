import copy
import math

from physics import TransformRB, Vector
from utils.errors import ImpossibleShotError
from visuals import ActiveImage


class Aircraft:
    def __init__(self, **kwargs):
        self.transform_rb = TransformRB(**kwargs)
        self.top_image = ActiveImage("./db/images/airship_top.png")
        self.side_image = ActiveImage("./db/images/airship_side.png")
        self.ship_length = 100


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


def angle_for_shot(g, v, yx):
    inner_sqrt = math.pow(v, 4) - g * (g * yx[1] * yx[1] + 2 * yx[0] * v * v)
    if inner_sqrt < 0:
        raise ImpossibleShotError("Impossible Shot")
    return math.atan2(v * v - math.sqrt(inner_sqrt), g * yx[1])


def to_plane(vector: Vector) -> (float, float):
    y = vector.y
    x = math.sqrt(vector.x * vector.x + vector.z * vector.z)
    return y, x


def shot_difficulty(a: Aircraft, b: Aircraft, shot_vector: Vector):
    shot_vector.rotate(a.transform_rb.rotation)

    relative_position = Vector(b.transform_rb.position).add(Vector(a.transform_rb.position).negate())
    relative_velocity = Vector(b.transform_rb.position_d).add(Vector(a.transform_rb.position_d).negate())

    initial_shot_vertical_angle = math.atan2(*to_plane(shot_vector))
    initial_shot_horizontal_angle = math.atan2(shot_vector.z, shot_vector.x)

    g = -a.transform_rb.gravity
    v = shot_vector.magnitude()

    yx = to_plane(relative_position)
    try:
        no_velocity_vertical_angle = angle_for_shot(g, v, yx)
    except ImpossibleShotError:
        no_velocity_vertical_angle = None

    current_position = Vector(relative_position)

    i_time = 0

    t = 0

    while True:
        yx = to_plane(current_position)
        try:
            vertical_angle = angle_for_shot(g, v, yx)
            t = yx[1] / (math.cos(vertical_angle) * v)
        except ImpossibleShotError:
            i_time += 0.5
            if i_time > 60:
                raise ImpossibleShotError("Impossible Shot Within 60 seconds")
            current_position = Vector(relative_position).add(Vector(relative_velocity).multiply(i_time))
            continue
        if yx[1] == 0:
            t = 0.00001
        temp_position = Vector(relative_position).add(Vector(relative_velocity).multiply(t))

        if Vector(current_position).add(Vector(temp_position).negate()).magnitude() < 0.1:
            break
        current_position = temp_position

    print(temp_position.comps)
    print(t)

    # size_bonus = 2 * math.log2(2 * math.atan2(s, 2 * math.sqrt(x * x + y * y)) / math.pi) + 12
    #
    # base_ange = math.atan2(y, x)
    # shot_angle = math.atan2(v * v - math.sqrt(math.pow(v, 4) - g * (g * x * x + 2 * y * v * v)), g * x)
    #
    # grav_bonus = - math.pow(24 * (shot_angle - base_ange) / math.pi, 2)
    #
    # bonus = size_bonus + grav_bonus



if __name__ == '__main__':
    print("start")
    shot_difficulty(Aircraft(), Aircraft(position=Vector((50, 0, 0)), position_d=Vector((-40, 0, 0))), Vector((20, 0, 0)))
