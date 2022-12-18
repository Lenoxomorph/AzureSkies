import math
import pickle
from io import BytesIO
from typing import Tuple, List

import discord
import numpy
from PIL import Image

from aircraft_rendering.aircraft import Aircraft
from aircraft_rendering.physics import Vector
from aircraft_rendering.visuals import ActiveImage


class Maps:
    def __init__(self, message_id, **kwargs):
        self.message_id = message_id
        self.canvases = [Canvas(f"./db/images/airship_bg_{x}.png", bool(x), **kwargs) for x in range(2)]
        self.aircrafts = [Aircraft()]

    def update(self):
        for aircraft in self.aircrafts:
            aircraft.transform_rb.update()

    def zoom(self, is_zoom_in):
        for canvas in self.canvases:
            canvas.pxl_per_ft *= 1.25 if is_zoom_in else 0.8

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
            self.canvases[x].render(self.aircrafts).save(image_binary, 'PNG')
            image_binary.seek(0)
            files.append(discord.File(fp=image_binary, filename=f'map{x}.png'))
        return files


class Canvas:
    def __init__(self, path: str, is_side: bool, pxl_per_ft: float = 1.6, camera_coords: Tuple[float] = (0, 0),
                 angle_from_north: float = 0):
        self.background = ActiveImage(path)
        self.is_side = is_side
        self.pxl_per_ft = pxl_per_ft
        self.camera_coords = camera_coords
        self.angle_from_north = angle_from_north

    def render(self, aircrafts: List[Aircraft]):
        canvas_image = self.background.image().copy()

        for aircraft in sorted(aircrafts, key=lambda a: a.transform_rb.position.comps[self.is_side + 1]):
            if self.is_side:
                aircraft_image = aircraft.side_image.image().copy()
                if 90 < aircraft.transform_rb.rotation.comps[2] % 360 < 270:
                    aircraft_image = aircraft_image.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)

                coords = aircraft.transform_rb.position.comps[:2]
                angle = aircraft.transform_rb.rotation.comps[1]
            else:
                aircraft_image = aircraft.top_image.image().copy()

                coords = aircraft.transform_rb.position.comps[::2]
                angle = -aircraft.transform_rb.rotation.comps[2]

            coords = numpy.add(coords, self.camera_coords)

            coords = list(coords)
            coords[1] *= -1

            new_width = aircraft.ship_length * self.pxl_per_ft
            new_height = aircraft_image.height * new_width / aircraft_image.width

            aircraft_image = aircraft_image.resize((int(new_width), int(new_height)), Image.Resampling.BICUBIC)
            aircraft_image = aircraft_image.rotate(angle, Image.Resampling.BICUBIC, expand=True)

            coords = numpy.multiply(coords, self.pxl_per_ft)
            coords = numpy.add(coords, (canvas_image.width / 2, canvas_image.height / 2))

            coords = numpy.add(coords, (-aircraft_image.width / 2, -aircraft_image.height / 2))
            canvas_image.paste(im=aircraft_image, box=[int(x) for x in coords], mask=aircraft_image)
        return canvas_image

    # Flip code - 90 < angle % 360 < 270
    # Sort by key code - sorted(uts, key=lambda x: x.value)
    # Flip image code - .transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)

    # Int code - [int(x) for x in coords]

    def draw_component(self, image: ActiveImage, height: float, coords: Tuple[float] = (0, 0), rotation: float = 0):
        pass

    def draw_arrow(self, start: tuple, end: tuple, rgb: tuple):
        pass
