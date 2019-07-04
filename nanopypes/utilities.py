from functools import wraps
from collections import defaultdict




def defaults_from_attrs(*attr_args):
    """
    Helper decorator for dealing with Task classes with attributes which serve
    as defaults for `Task.run`.  Specifically, this decorator allows the author of a Task
    to identify certain keyword arguments to the run method which will fall back to `self.ATTR_NAME`
    if not explicitly provided to `self.run`.  This pattern allows users to create a Task "template",
    whose default settings can be created at initialization but overrided in individual instances when the
    Task is called.

    Args:
        - *attr_args (str): a splatted list of strings specifying which
            kwargs should fallback to attributes, if not provided at runtime. Note that
            the strings provided here must match keyword arguments in the `run` call signature,
            as well as the names of attributes of this Task.

    Returns:
        - Callable: the decorated / altered `Task.run` method

    Note: This is code from a python package called Prefect. I kept the docstring in as well because
    it is so nicely written. The example below is refering to Prefect classes, not Nanopypes.

    Example:
    ```python
    class MyTask(Task):
        def __init__(self, a=None, b=None):
            self.a = a
            self.b = b

        @defaults_from_attrs('a', 'b')
        def run(self, a=None, b=None):
            return a, b

    task = MyTask(a=1, b=2)

    task.run() # (1, 2)
    task.run(a=99) # (99, 2)
    task.run(a=None, b=None) # (None, None)
    ```
    """

    def wrapper(run_method):
        @wraps(run_method)
        def method(self, *args, **kwargs):
            for attr in attr_args:
                kwargs.setdefault(attr, getattr(self, attr))
            return run_method(self, *args, **kwargs)

        return method

    return wrapper


class CommandBuilder:
    """
    Class for generating command line command strings from a template. Templates are used to generate
    the command across partitioned data (for parallel processing).

    Args:
        - template (string): a string template with variables wrapped in brackets {}.
            (Example template: 'minimap2 -ax map-ont {ref} {read} -o {output}')
    """
    def __init__(self, commands, template_config):
        self.commands = commands
        self.template_config = template_config

        self.templates = {}
        for command in self.commands:
            self.generate_templates(command)


    def build_command(self, command, **kwargs):
        var_dict = defaultdict(str, kwargs)
        print("here: ", var_dict)
        print(command)
        print(self.templates[command])
        built_command = self.templates[command].format_map(var_dict)
        return built_command

    def generate_templates(self, command):
        config = self.template_config[command]
        template = ""
        command_order = config.pop('command_order')
        for cmd in command_order:
            template += (cmd + " ")
            template += (config.pop(cmd) + " ")

        for key, value in config.items():
            template += (key + " " + value + " ")

        self.templates[command] = template

#####################
# Exceptions
#####################

class SubprocessError(Exception):
    pass

class InValidTaskError(KeyError):
    pass


if __name__ == '__main__':
    # command_template = CommandBuilder('minimap2 -ax map-ont {ref} {read} -o {output}')
    # command = command_template.build(**{'read':'my_read'})
    command = "hi" + "\r" + "stranger"
    print(command)


