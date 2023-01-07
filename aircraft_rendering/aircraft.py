import math

from .physics import TransformRB, Vector
from utils.errors import ImpossibleShotError
from .visuals import ActiveImage


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
        raise ImpossibleShotError("Unknown Reason - Impossible Shot")
    return math.atan2(v * v - math.sqrt(inner_sqrt), g * yx[1])


def to_plane(vector: Vector) -> (float, float):
    y = vector.y
    x = math.sqrt(vector.x * vector.x + vector.z * vector.z)
    return y, x


def angle_distance(a1, a2):
    return (a2 - a1 - math.pi) % (2 * math.pi) - math.pi


def shot_difficulty(a: Aircraft, b: Aircraft, shot_vector: Vector, azimuth_min_max, elevation_min_max):
    shot_vector.rotate(a.transform_rb.rotation)

    relative_position = Vector(b.transform_rb.position).add(Vector(a.transform_rb.position).negate())
    relative_velocity = Vector(b.transform_rb.position_d).add(Vector(a.transform_rb.position_d).negate())

    initial_shot_horizontal_angle = math.atan2(shot_vector.z, shot_vector.x)
    initial_shot_vertical_angle = math.atan2(*to_plane(shot_vector))

    g = -a.transform_rb.gravity
    v = shot_vector.magnitude()

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

        if Vector(current_position).add(Vector(temp_position).negate()).magnitude() < 0.01:
            current_position = temp_position
            break
        current_position = temp_position

    s = b.ship_length

    yx = to_plane(relative_position)
    yx2 = to_plane(current_position)

    horizontal_angle = math.atan2(current_position.z, current_position.x)
    try:
        vertical_angle = angle_for_shot(g, v, yx2)
    except ImpossibleShotError:
        raise ImpossibleShotError("Impossible Shot (Last Second)")

    if not azimuth_min_max[0] < angle_distance(initial_shot_horizontal_angle, horizontal_angle) < azimuth_min_max[1]:
        raise ImpossibleShotError("Out of range horizontally")
    if not elevation_min_max[0] < angle_distance(initial_shot_vertical_angle, vertical_angle) < elevation_min_max[1]:
        raise ImpossibleShotError("Out of range vertically")

    size_bonus = 2 * math.log2(2 * math.atan2(s, 2 * current_position.magnitude()) / math.pi) + 12

    grav_bonus = - math.pow(24 * abs(angle_distance(math.atan2(*yx2), vertical_angle)) / math.pi, 2)

    no_velocity_horizontal_angle = math.atan2(relative_position.z, relative_position.x)
    try:
        no_velocity_vertical_angle = angle_for_shot(g, v, yx)
    except ImpossibleShotError:
        vertical_bonus = -10
    else:
        vertical_bonus = -32 * abs(angle_distance(no_velocity_vertical_angle, vertical_angle)) / math.pi
    horizontal_bonus = -32 * abs(angle_distance(no_velocity_horizontal_angle, horizontal_angle)) / math.pi

    velocity_bonus = vertical_bonus + horizontal_bonus

    return size_bonus, grav_bonus, velocity_bonus


if __name__ == '__main__':
    print("start")
    while True:
        print(shot_difficulty(Aircraft(rotation=Vector((0, -45, 0)), position_d=Vector((50, 0, 0))), Aircraft(position=Vector((50, 0, 0)), position_d=Vector((0, 0, 50))),
                              Vector((600, 0, 0)), (-1.39626, 1.39626), (-0.174533, 1.39626)))
