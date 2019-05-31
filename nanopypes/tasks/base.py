


class Task():

    def __init__(self, name=None):
        self.name = name

    def run(self):
        pass

    @classmethod
    def from_dict(cls, config_dict):
        instance = cls.__new__(cls)
        instance.__dict__.update(config_dict)
        return instance

