

class Pipeline:
    def __init__(self, pipes):
        self.pipes = pipes

    def __call__(self):
        for pipe in self.pipes:
            pipe()


class Pipe():

    def __init__(self):
        pass

    def execute(self):
        pass

    @classmethod
    def from_dict(cls, config_dict):
        instance = cls.__new__(cls)
        instance.__dict__.update(config_dict)
        return instance

    def __call__(self):
        return self.execute()


