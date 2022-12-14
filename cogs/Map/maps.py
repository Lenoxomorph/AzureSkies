import pickle
from io import BytesIO
from typing import Tuple

import discord

from aircraft.visuals import ActiveImage


class Maps:
    def __init__(self, message_id, **kwargs):
        self.message_id = message_id
        self.canvases = [Canvas(f"./db/images/airship_bg_{x}.png", **kwargs) for x in range(2)]
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
            self.canvases[x].render().save(image_binary, 'PNG')
            image_binary.seek(0)
            files.append(discord.File(fp=image_binary, filename=f'map{x}.png'))
        return files


class Canvas:
    def __init__(self, path: str, pxl_per_ft: int = 5, camera_coords: Tuple[int] = (0, 0), angle_from_north: int = 0):
        self.background = ActiveImage(path)
        self.pxl_per_ft = pxl_per_ft
        self.camera_coords = camera_coords
        self.angle_from_north = angle_from_north

    def render(self):
        return self.background.image()

    def draw_arrow(self, start: tuple, end: tuple, rgb: tuple):
        pass
