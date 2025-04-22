    # decorated messages:

    def _boxprint_linux(self, s):
        n = len(s)+2
        self.print()
        self.print(f"┌{'─'*n}┐")
        self.print(f"│ { s } │")
        self.print(f"└{'─'*n}┘")
        self.print()
        return

    def _boxprint_default(self, s):
        n = len(s)+2
        self.print()
        self.print(f"#{'#'*n}#")
        self.print(f"# { s } #")
        self.print(f"#{'#'*n}#")
        self.print()
        return


        # os dependent configuration
        from platform import system as _OS
        _CONFIG = {
            'Linux'  : {'boxprint': self._boxprint_linux},
            'Darwin' : {'boxprint': self._boxprint_default},
            'Windows': {'boxprint': self._boxprint_default},

        }[_OS()]
        
        # os dependent setup
        self.boxprint = _CONFIG['boxprint']
