import sys
import re
from typing import List
from cath_request import CathRequest


class CathCli:
    def __init__(self):
        if len(sys.argv) < 2:
            print("Invalid Input")
            sys.exit()
        else:
            self.args: List[str] = sys.argv[1:]
        self.usage = ''

    def cli(self):
        superfamily_id = self.args[0]
        cath = CathRequest(superfamily_id)
        if not _input_pattern(superfamily_id):
            print("Invalid Superfamily ID")
            sys.exit()
        if len(self.args) > 2:
            print(f"The maximum number of arguments is 2, you inputed {len(self.args)} arguments")
            print(self.usage)
            sys.exit()
        elif len(self.args) < 1:
            print("You must put at least 1 argument")
            print(self.usage)
            sys.exit()
        elif len(self.args) == 1:
            cath.run(opt=1, funfam_id=0)
        else:
            try:
                funfam = int(self.args[1])
                cath.run(opt=2, funfam_id=funfam)
            except ValueError:
                print("You must put a number representative of a functional family for this superfamily")


def _input_pattern(string):
    pattern = r'^[0-9.]+$'
    match = re.match(pattern, string)
    if match:
        return True
    else:
        return False


if __name__ == '__main__':
    cli_tool = CathCli()
    cli_tool.cli()
    