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
    def __init__(self, message_id, altitude: float, pxl_per_ft: float = 1.6, camera_coords: Tuple[float] = (0, 0, 0),
                 angle_from_north: float = 0):
        self.message_id = message_id
        self.altitude = altitude
        self.canvases = [Canvas(f"./db/images/airship_bg_{x}.png", bool(x)) for x in range(2)]
        a1 = Aircraft(mass=1, position=Vector((300, 0, 0)))
        a2 = Aircraft(mass=1)
        self.aircrafts = [a1, a2]

        self.pxl_per_ft = pxl_per_ft
        self.camera_coords = camera_coords
        self.angle_from_north = angle_from_north

    def update(self):
        for aircraft in self.aircrafts:
            print(aircraft)
            aircraft.transform_rb.update(self.altitude)

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
        self.is_side = is_side

    def render(self, aircrafts: List[Aircraft], maps: Maps):
        canvas_image = self.background.image().copy()

        for aircraft in sorted(aircrafts, key=lambda a: a.transform_rb.position.comps[self.is_side + 1],
                               reverse=self.is_side):
            if self.is_side:
                aircraft_image = aircraft.side_image.image().copy()
                if 90 < aircraft.transform_rb.rotation.comps[2] % 360 < 270:
                    aircraft_image = aircraft_image.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)

                coords = aircraft.transform_rb.position.comps[:2]
                camera_coords = maps.camera_coords[:2]
                angle = aircraft.transform_rb.rotation.comps[1]
            else:
                aircraft_image = aircraft.top_image.image().copy()

                coords = aircraft.transform_rb.position.comps[::2]
                camera_coords = maps.camera_coords[::2]
                angle = -aircraft.transform_rb.rotation.comps[2]

            coords = numpy.subtract(coords, camera_coords)
            coords = list(coords)
            coords[1] *= -1

            new_width = aircraft.image_length * maps.pxl_per_ft
            new_height = aircraft_image.height * new_width / aircraft_image.width

            aircraft_image = aircraft_image.resize((int(new_width), int(new_height)), Image.Resampling.BICUBIC)
            aircraft_image = aircraft_image.rotate(angle, Image.Resampling.BICUBIC, expand=True)

            coords = numpy.multiply(coords, maps.pxl_per_ft)
            coords = numpy.add(coords, (canvas_image.width / 2, canvas_image.height / 2))

            # print(coords)
            # if not (0 <= coords[0] <= canvas_image.width and 0 <= coords[1] <= canvas_image.height):

            coords = numpy.add(coords, (-aircraft_image.width / 2, -aircraft_image.height / 2))
            canvas_image.paste(im=aircraft_image, box=[int(x) for x in coords], mask=aircraft_image)
        return canvas_image

    # Flip code - 90 < angle % 360 < 270
    # Sort by key code - sorted(uts, key=lambda x: x.value)
    # Flip image code - .transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)

    # Int code - [int(x) for x in coords]

    def draw_component(self, canvas: Image.Image, image: Image.Image, width: float, coords: Tuple[float] = (0, 0),
                       rotation: float = 0):
        pass

    def draw_arrow(self, canvas: Image.Image, start: tuple, end: tuple, rgb: tuple):
        pass
        pil_image = Image.open('Image.jpg').convert('RGB')
        open_cv_image = numpy.array(pil_image)
        # Convert RGB to BGR
        open_cv_image = open_cv_image[:, :, ::-1].copy()
