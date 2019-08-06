from spython.main import Client

from prefect import Task
from prefect.utilities.tasks import defaults_from_attrs


class PullImage(Task):
    def __init__(self, image_url=None, save_path=None, **kwargs):
        super().__init__(**kwargs)
        self.image_url = image_url
        self.save_path = save_path

    @defaults_from_attrs('image_url', 'save_path')
    def run(self, image_url=None, save_path=None):
        image = Client.pull(image_url, pull_folder=save_path)
        print(image)


class BatchSingularityExecute(Task):
    def __init__(self, commands=None, image_path=None, bind_paths=None, **kwargs):
        super().__init__(**kwargs)
        self.commands = commands
        self.image_path = image_path
        self.bind_paths = bind_paths

    @defaults_from_attrs('commands', 'image_path', 'bind_paths')
    def run(self, commands=None, image_path=None, bind_paths=None):
        Client.load(image_path)
        all_outs = []
        all_error_messages = []
        failure = False
        for i, c in enumerate(commands):
            if isinstance(c, str):
                command = c.split()
            else: command = c

            stdout = Client.execute(image_path, command, bind=bind_paths, return_result=True)
            if stdout['return_code'] !=0:
                all_error_messages.append(stdout['message'])
                failure = True
            elif stdout['return_code'] == 0:
                all_outs.append(stdout['message'])
        return all_outs


if __name__ == '__main__':
    from prefect import Flow
    bc = ExecuteBatchCommands()

    with Flow('my-flow') as flow:
        bc(commands=["ls", "cd .."], image_path="./hello-world.sif", bind_paths=".")
    flow.run()
