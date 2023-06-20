import sys
from typing import List
from cath_request import CathRequest


class CathCli:
    def __init__(self):
        self.args: List[str] = sys.argv[1:]
        self.usage = ''

    def cli(self):
        #funfam = self.args[1]

        if len(self.args) > 2:
            print(f"The maximum number of arguments is 2, you inputed {len(self.args)} arguments")
            print(self.usage)
            sys.exit()
        if len(self.args) < 1:
            print("You must put at least 1 argument")
            print(self.usage)
            sys.exit()
        elif len(self.args) == 1:
            superfamily_id = self.args[0]
            cath = CathRequest(superfamily_id)
            cath.get_info()


if __name__ == '__main__':
    cli_tool = CathCli()
    cli_tool.cli()
