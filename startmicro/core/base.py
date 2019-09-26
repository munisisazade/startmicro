import os
import sys
import subprocess
from startmicro.core.utils.questions import prompt, style, questions
from startmicro.core.utils.detect import os_type


class Command(object):
    """
        Application base logic class
    """

    def __init__(self, folder_name):
        """
            Initialize folder name
        """
        self.folder_name = folder_name
        self.path = "%s/" % folder_name if os_type != "Windows" else "%s\\" % folder_name

    def run(self):
        self.create_folder()  # Create application Folder
        # First Create virtualenv folder
        answers = prompt(questions, style=style)
        print(answers)
        if os_type == "Windows":
            pass
        else:  # Mac or Linux
            pass

    def run_win_cmd(self, commands):
        result = []
        process = subprocess.Popen(commands,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        for line in process.stdout:
            result.append(line)
        errcode = process.returncode
        for line in result:
            sys.stdout.write(line.decode("utf-8"))
        if errcode is not None:
            raise Exception('cmd %s failed, see above for details', commands)

    def create_folder(self):
        os.makedirs(self.folder_name)
