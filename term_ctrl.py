import sys

class TerminalControler():
    def __init__(self, log = False, progress = True):
        self.log = log
        self.prgrs = progress

    def progress(self, end = False):
        if self.prgrs:
            self.show("|\n" if end else "|▒", force_activ=True)
            self.flush()

    def show(self, msg, force_activ = False, end = False):
        end = "\n" if end else ""
        if (force_activ) or (self.log):
            print(msg, end = end)

    def flush(self):
        sys.stdout.flush()
    