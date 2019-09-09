import os
import subprocess
import tempfile
import logging
from typing import Any, List, Callable

import prefect
from prefect.utilities.tasks import defaults_from_attrs
from prefect.utilities.logging import get_logger

from nanopypes.utilities import CommandBuilder
from nanopypes.distributed_data.partition_data import extract_partitioned_directories


class ShellTransformTask(prefect.Task):
    def __init__(
        self,
        data: list = None,
        batch_num: int = None,
        env: dict = None,
        template: str = None,
        save_path: str = None,
        helper_script: str = None,
        shell: str = "bash",
        extract_fn: Callable = None,
        is_initial: bool = False,
        fn_kwargs: dict = None,
        **kwargs: Any
    ):
        self.data = data
        self.batch_num = batch_num
        self.env = env
        self.template = template
        self.save_path = save_path
        self.helper_script = helper_script
        self.shell = shell
        self.extract_fn = extract_fn
        self.is_initial = is_initial
        self.fn_kwargs = fn_kwargs
        super().__init__(**kwargs)

    @defaults_from_attrs("data", "env", "template", "batch_num", "fn_kwargs", "is_initial", "extract_fn", "save_path")
    def run(self, data: list = None,
            batch_num: int = None,
            env: dict = None,
            template: str = None,
            save_path: str = None,
            fn_kwargs: dict =None,
            extract_fn: Callable = None,
            is_initial: bool = False) -> bytes:
        """
        Run the shell command.
        Args:
            - command (string): shell command to be executed; can also be
                provided at task initialization. Any variables / functions defined in
                `self.helper_script` will be available in the same process this command
                runs in
            - env (dict, optional): dictionary of environment variables to use for
                the subprocess
        Returns:
            - stdout + stderr (bytes): anything printed to standard out /
                standard error during command execution
        Raises:
            - prefect.engine.signals.FAIL: if command has an exit code other
                than 0
        """
        if data is None or data == []:
            raise TypeError("run() missing required argument: 'command'")

        current_env = os.environ.copy()
        current_env.update(env or {})
        logger = prefect.context.get("logger")

        failure = False

        if is_initial:
            # command_data = data[batch_num]["command_data"]
            # batch_saves = data[batch_num]["saves"]
            input_data = data[batch_num]
        else:
        #     command_data = data["command_data"]
            input_data = data
        #     batch_saves = data["saves"]

        transform_data = self._extract_data(extract_fn, input_data, save_path)
        cb = CommandBuilder(template)
        command_data = transform_data.pop("command_data")

        for cd in command_data:  # [batch_num]:
            command = cb.build_command(cd)
            #all_commands.append(command)
            print("COMMAND: ", command)
            logger.info("Beginning to run ShellTransformTask with command '{}' on batch number {}".format(command, batch_num))

            with tempfile.NamedTemporaryFile(prefix="prefect-") as tmp:
                if self.helper_script:
                    tmp.write(self.helper_script.encode())
                    tmp.write("\n".encode())
                tmp.write(command.encode())
                tmp.flush()
                try:
                    logger.info(
                        "Beginning to run ShellTransformTask with command '{}' on batch number {}".format(command, batch_num))
                    out = subprocess.check_output(
                        [self.shell, tmp.name], stderr=subprocess.STDOUT, env=current_env
                    )
                    logger.info(
                        "Finished run ShellTransformTask with command '{}' on batch number {}".format(command, batch_num))
                    #all_outs.append(out)
                except subprocess.CalledProcessError as exc:
                    error_msg = "Command '{command}' failed with exit code {0}: {1}".format(
                        exc.returncode, exc.output, command=command
                    )
                    #all_error_messages.append(error_msg)
                    failure = True

        if failure:
            raise prefect.engine.signals.FAIL(error_msg) from None  # type: ignore

        #results = extract_fn(batch_saves, batch_num, **fn_kwargs)
        # if is_initial:
        #     results = results[batch_num]
        # input_data['inputs'][self.task_id] = results[1]

        return transform_data #{'inputs': input_data, 'saves': results[2], 'command_data': results[0]}

    def _extract_data(self, extract_fn, input_data, save_path):

        # save_path = os.path.join(save_path, self.name)
        #
        # if os.path.exists(save_path) is False:
        #     os.mkdir(save_path)
        command_data = extract_fn(input_data, save_path, self.name)
        return command_data





