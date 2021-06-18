class TablePrinter:
    def __init__(self, content):
        self.content = content

    def print(self):
        s = ""
        out = ""
        for i, chord in enumerate(self.content):
            if i % 4 == 0 and s != "":
                out += "|" + s + "\n"
                s = ""
            s += " {:<8} |".format(chord)
        out += "|" + s
        return out
