from spython.main import Client


class PipeClient:

    def execute(self):
        pass


class SingularityClient(PipeClient):

    def __init__(self):
        self.client = Client
        self.image = None

    def execute(self, command, image=None, link=None, pull=False, bind=None):
        if pull:
            self.image = self.pull(link)
        stdout = self.client.execute(self.image, command, bind=bind)
        print(stdout)
        return stdout

    def pull(self, container_file=None):
        if container_file == None:
            container_file = self.container_file
        self.image = self.client.pull(container_file)

        return self.image

if __name__ == '__main__':
    client = SingularityClient()
    image = client.pull('docker://genomicpariscentre/guppy')
    client.execute(["guppy_basecaller"], image, bind="/path")


