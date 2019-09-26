import os
import sys
import string
from startmicro.core.base import Command
from startmicro.core.command import CommandParser
from startmicro.core.utils.color import color_style
from startmicro import __version__, __author__


class ManagementUtility(object):
    """
        Encapsulate the logic of the CLI utilities.
    """

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.style = color_style()
        self.folder_name = None
        punk = string.punctuation
        punk = punk.replace("_", "")
        punk = punk.replace("-", "")
        self.caracters = punk
        if self.prog_name == '__main__.py':
            self.prog_name = 'python -m startmicro'
        self.settings_exception = None
        self.issue_url = "https://github.com/munisisazade/startmicro"
        self.argument_list = (
            ('-V', '--version', self.get_version),
            ('-l', '--log', self.get_logging),
            ('-a', '--author', self.get_author),
            ('-g', '--git', self.get_version)
        )

    def main_help_text(self, commands_only=False):
        """Return the script's main help text, as a string."""
        usage = [
            "",
            "😄 %s is a CLI tool that provisions and manages Microservice Flask application optimized for development workflows." % self.prog_name,
            "",
            "Usage:",
            "   %s [folder_name]" % self.prog_name,
            "",
            "Available Commands:",
            *self.get_commands(),
            "",
            "Flags:",
            *self.get_flags(),
            ""
        ]

        return '\n'.join(usage)

    def unknown_command(self):
        """Return the script's when command unknown"""
        for_example_list = [
            "Only accept `_` or `-` punctuation",
            "Please use : %s for folder_name" % self.folder_name.translate(str.maketrans('','',self.caracters))
        ]

        usage = [
            "",
            "😿 Error: cannot accept `%s` for folder_name" % self.folder_name,
            "",
            *for_example_list,
            "Run '%s --help' for usage." % self.prog_name,
            # "👉👉👉👉👉👉Run '%s --help' for usage." % self.prog_name,
            ""
        ]
        return '\n'.join(usage)

    def file_exist(self):
        """Return the script's when command unknown"""
        usage = [
            "",
            "😿 Error:  `%s` %s already exist " % (self.folder_name, "folder" if self.dir else "file"),
            "",
            "Run '%s --help' for usage." % self.prog_name,
            ""
        ]
        return '\n'.join(usage)

    def check_file_exist(self):
        self.dir = True if os.path.isdir(self.folder_name) else False
        if os.path.isdir(self.folder_name) or os.path.isfile(self.folder_name):
            sys.stdout.write(self.file_exist())
            sys.exit(1)
        else:
            pass

    def run_args(self, args):
        flag = args[0]
        for first_flag, second_flag, func in self.argument_list:
            if first_flag == flag or second_flag == flag:
                func()
                break
        else:
            text = [
                "Wrong flag name `%s` " % flag,
                "Use bellow flag list: ",
                ""
            ]
            sys.stdout.write("\n".join(text))
            sys.stdout.write('\n'.join(self.get_flags()))

    def execute(self):
        """
            Given the command-line arguments, figure out which subcommand is being
            run, create a parser appropriate to that command, and run it.
        """
        parser = CommandParser(None, usage="%(prog)s subcommand [options] [args]", add_help=False)
        parser.add_argument('args', nargs='*')  # catch-all
        options, args = parser.parse_known_args(self.argv[1:])

        if args:
            self.run_args(args)

        if len(options.args) == 1:
            self.folder_name = options.args[0]
            if self.folder_name.isalnum():
                self.check_file_exist()
                cmd = Command(self.folder_name)
                cmd.run()
                sys.stdout.write("\n")
                sys.stdout.write(" Successfuly created {}\n".format(self.folder_name))
                sys.stdout.write("\n")
                sys.stdout.write(" Start microservice bellow commands :\n")
                sys.stdout.write("\n")
                sys.stdout.write("  cd {}\n".format(self.folder_name))
                sys.stdout.write("\n")
                sys.stdout.write("  source .venv/bin/activate\n")
                sys.stdout.write("  pip install -r requirements.txt\n")
                sys.stdout.write("  python run.py\n")
                sys.stdout.write("\n")
                sys.stdout.write("  If you have any problems, do not hesitate to file an issue:\n")
                sys.stdout.write("    {}\n".format(self.issue_url))
            else:
                name = self.folder_name
                name = name.translate(str.maketrans('', '', string.ascii_letters + string.digits))
                if list(set(name) & set(self.caracters)):
                    sys.stdout.write(self.unknown_command())
                    sys.exit(1)
                else:
                    cmd = Command(self.folder_name)
                    cmd.run()
        elif len(options.args) > 1:
            sys.stdout.write("Note: only one argument accepted folder_name")
            sys.stdout.write(self.main_help_text())
            sys.exit(1)
        else:
            sys.stdout.write(self.main_help_text())
            sys.exit(1)

    def get_commands(self):
        return [
            "   folder_name         Application name and base project directory space not allow"
        ]

    def get_flags(self):
        return [
            "   -V, --version       Get %s CLI version" % self.prog_name,
            "   -l, --log           Print aditional logs",
            "   -a, --author        Print author's info",
            "   -g, --git           Application integrate git",
            ""
        ]

    def get_version(self):
        text = [
            "%s CLI tool" % self.prog_name,
            "Current version: %s" % __version__,
            "Thanks for using :)",
            ""
        ]
        sys.stdout.write("\n".join(text))
        sys.exit(1)

    def get_logging(self):
        text = [
            "%s CLI tool" % self.prog_name,
            "Logging coming soon",
            "Thanks for using :)",
            ""
        ]
        sys.stdout.write("\n".join(text))
        sys.exit(1)

    def get_author(self):
        text = [
            "%s CLI tool" % self.prog_name,
            "Author : %s" % __author__,
            "Thanks for using :)",
            ""
        ]
        sys.stdout.write("\n".join(text))
        sys.exit(1)


def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    utility = ManagementUtility(argv)
    utility.execute()
