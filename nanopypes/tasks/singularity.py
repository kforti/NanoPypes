from spython.main import Client

from prefect import Task
from prefect.utilities.tasks import defaults_from_attrs


class SingularityTask(Task):
    def __init__(self, command=None, image_path=None, pull=False, bind=None):
        self.command = command
        self.image_path = image_path
        self.pull = pull
        self.bind = bind

    @defaults_from_attrs('command', 'image_path', 'pull', 'bind')
    def run(self, command=None, image_path=None, pull=False, bind=None):
        if pull:
            image = self.pull(image_path)
        stdout = self.client.execute(image, command, bind=bind)
        return stdout

    def _pull(self, link):
        image = self.client.pull(link)
        return image

