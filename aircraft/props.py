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
