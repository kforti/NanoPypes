from spython.main import Client


class PipeClient:

    def execute(self):
        pass


class SingularityClient(PipeClient):

    def __init__(self):
        self.client = Client

    def execute(self, cmd, image=None, link=None, pull=False, bind=None):
        if pull:
            image = self.pull(link)
        stdout = self.client.execute(image, cmd, bind=bind)
        return stdout

    def pull(self, link):
        image = self.client.pull(link)
        return image

if __name__ == '__main__':
    client = SingularityClient()
    image = client.pull('docker://genomicpariscentre/guppy')
    client.execute(["guppy_basecaller"], image, bind="/path")


