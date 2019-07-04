import subprocess
import os
import tempfile

from dagster import lambda_solid

from nanopypes.utilities import defaults_from_attrs, SubprocessError
from nanopypes.tasks import Task


class ShellTask(Task):

    def __init__(self, command=None, env=None, helper_script=None,
                 shell="bash", **kwargs):
        super().__init__(**kwargs)
        self.command = command
        self.env = env
        self.helper_script = helper_script
        self.shell = shell

    @defaults_from_attrs('command', 'env')
    def run(self, command=None, env=None, *dependencies):
        if command is None:
            raise TypeError("run() missing required argument: 'command'")

        current_env = os.environ.copy()
        current_env.update(env or {})
        with tempfile.NamedTemporaryFile(prefix="nanopypes-") as tmp:
            if self.helper_script:
                tmp.write(self.helper_script.encode())
                tmp.write("\n".encode())
            tmp.write(command.encode())
            tmp.flush()
            try:
                out = subprocess.check_output(
                    [self.shell, tmp.name], stderr=subprocess.STDOUT, env=current_env
                )
            except subprocess.CalledProcessError as exc:
                msg = "Command failed with exit code {0}: {1}".format(
                    exc.returncode, exc.output
                )
                raise SubprocessError(msg)
        return out





