from PIL import Image


class ActiveImage:
    def __init__(self, path: str):
        self.path = path
        self.cached_image = None

    def image(self):
        if self.cached_image is None:
            self.cached_image = Image.open(self.path)
        return self.cached_image

    def clear_cache(self):
        self.cached_image = None
