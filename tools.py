


class debug_new():

    def __init__(self, *flags):
        self.flags = [f.upper() for f in flags]
        print(self.flags)
        return

    def flag(self, *flags):
        if "NONE" in self.flags:
            return False
        if "ALL" in self.flags:
            return True
        for f in flags:
            if f.upper() in self.flags:
                return True
        if flags:
            return False
        return True
