import pickle
from io import BytesIO
from typing import Tuple, List

import cv2
import discord
import numpy
from PIL import Image

from aircraft_rendering.aircraft import Aircraft
from aircraft_rendering.physics import Vector
from aircraft_rendering.visuals import ActiveImage


class Maps:
    def __init__(self, message_id, altitude: float, camera_coords: Vector, pxl_per_ft: float = 1.6,
                 angle_from_north: float = 0):
        self.message_id = message_id
        self.altitude = altitude
        self.canvases = [Canvas(f"./db/images/airship_bg_{x}.png", bool(x)) for x in range(2)]
        a1 = Aircraft(mass=100, drag_profiles=Vector((1, 1, 1)), position=Vector((0, 0, 0)), position_d=Vector(),
                      rotation=Vector((0, 0, 90)))
        a2 = Aircraft(mass=100, drag_profiles=Vector((1, 1, 1)), position=Vector((300, 0, 0)), position_d=Vector(),
                      rotation=Vector())
        self.aircrafts = [a1, a2]

        self.pxl_per_ft = pxl_per_ft
        self.camera_coords = camera_coords
        self.angle_from_north = angle_from_north
        self.if_vector_arrows = True

    def update(self):
        for aircraft in self.aircrafts:
            print(aircraft)
            aircraft.transform_rb.update(self.altitude, force=Vector(), relative_force=Vector(), wind_velocity=Vector(),
                                         rotation=Vector())

    def save(self):
        for canvas in self.canvases:
            canvas.background.clear_cache()
        for aircraft in self.aircrafts:
            aircraft.top_image.clear_cache()
            aircraft.side_image.clear_cache()
        with open(f"./db/maps/map_{self.message_id}.pckl", 'wb') as f:
            pickle.dump(self, f)

    def render_files(self):
        files = []
        for x in range(2):
            image_binary = BytesIO()
            self.canvases[x].render(self.aircrafts, self).save(image_binary, 'PNG')
            image_binary.seek(0)
            files.append(discord.File(fp=image_binary, filename=f'map{x}.png'))
        return files


class Canvas:
    def __init__(self, path: str, is_side: bool):
        self.background = ActiveImage(path)
        self.canvas = None
        self.is_side = is_side

    def render(self, aircrafts: List[Aircraft], maps: Maps):
        self.canvas = self.background.image().copy()

        for aircraft in sorted(aircrafts, key=lambda a: a.transform_rb.position.comps[self.is_side + 1],
                               reverse=self.is_side):
            angle = aircraft.transform_rb.rotation
            angle = angle.y if self.is_side else -angle.z

            coords = self.draw_component(aircraft.render(self.is_side), maps, aircraft.image_length,
                                         aircraft.transform_rb.position, angle)

            # print(coords)
            # if not (0 <= coords[0] <= canvas_image.width and 0 <= coords[1] <= canvas_image.height):

            if maps.if_vector_arrows:
                self.draw_arrow(coords, numpy.add(coords, self.coords_from_vector(
                    Vector(aircraft.transform_rb.position_d).multiply(maps.pxl_per_ft))), (0, 0, 0, 255))

        return self.canvas

    def coords_from_vector(self, vector: Vector):
        coords: List[float] = list(vector.comps[:2] if self.is_side else vector.comps[::2])
        coords[1] *= -1
        return coords

    # Flip code - 90 < angle % 360 < 270
    # Sort by key code - sorted(uts, key=lambda x: x.value)
    # Flip image code - .transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)

    # Int code - [int(x) for x in coords]

    def draw_component(self, image: Image.Image, maps: Maps, width: float, vector: Vector, rotation: float = 0):
        vector = Vector(vector).add(Vector(maps.camera_coords).negate())
        coords = self.coords_from_vector(vector)

        new_width = width * maps.pxl_per_ft
        new_height = image.height * new_width / image.width

        image = image.resize((int(new_width), int(new_height)), Image.Resampling.BICUBIC)
        image = image.rotate(rotation, Image.Resampling.BICUBIC, expand=True)

        coords = numpy.multiply(coords, maps.pxl_per_ft)
        coords = numpy.add(coords, (self.canvas.width / 2, self.canvas.height / 2))

        draw_coords = numpy.add(coords, (-image.width / 2, -image.height / 2))
        self.canvas.paste(im=image, box=[int(x) for x in draw_coords], mask=image)

        return tuple(coords)

    def draw_arrow(self, start: tuple, end: tuple, rgba: tuple):
        # noinspection PyTypeChecker
        self.canvas = Image.fromarray(
            cv2.arrowedLine(numpy.array(self.canvas), self.float_tuple_to_int(start), self.float_tuple_to_int(end),
                            rgba, 8))

    @staticmethod
    def float_tuple_to_int(t: Tuple[float]):
        return int(t[0]), int(t[1])
