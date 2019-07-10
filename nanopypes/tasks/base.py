from prefect import Task


class Task(Task):

    def __init__(self, name=None, **kwargs):
        self.name = name
        super().__init__(**kwargs)

    @classmethod
    def from_dict(cls, config_dict):
        instance = cls.__new__(cls)
        instance.__dict__.update(config_dict)
        return instance
