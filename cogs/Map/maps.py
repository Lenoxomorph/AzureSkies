import pickle
from io import BytesIO
from typing import Tuple

import discord

from aircraft_rendering.visuals import ActiveImage


def top_aircraft_handler():
    pass


def side_aircraft_handler():
    pass


class Maps:
    def __init__(self, message_id, **kwargs):
        self.message_id = message_id
        self.canvases = [Canvas(f"./db/images/airship_bg_{x}.png", function, **kwargs)
                         for x, function in enumerate([top_aircraft_handler, side_aircraft_handler])]
        self.aircrafts = None  # List[Aircraft]

    def save(self):
        for canvas in self.canvases:
            canvas.background.clear_cache()
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
    def __init__(self, path: str, get_aircraft_coords, pxl_per_ft: float = 5, camera_coords: Tuple[float] = (0, 0),
                 angle_from_north: float = 0):
        print(get_aircraft_coords)
        self.background = ActiveImage(path)
        self.get_aircraft_coords = get_aircraft_coords
        self.pxl_per_ft = pxl_per_ft
        self.camera_coords = camera_coords
        self.angle_from_north = angle_from_north

    def render(self, airships):
        return self.background.image()

    def draw_component(self, image: ActiveImage, height: float, coords: Tuple[float] = (0, 0), rotation: float = 0):
        pass

    def draw_arrow(self, start: tuple, end: tuple, rgb: tuple):
        pass
