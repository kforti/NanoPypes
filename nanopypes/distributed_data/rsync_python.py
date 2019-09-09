import os
import shutil
from prefect.tasks.shell import ShellTask

rsync_command = "rsync -azP {source} {destination}"
shutil.move
