
def process(self):
    self.replace("SYMBOL")
    self.replace("-", " ")
    self.camelCase()
    pass
    

if __name__ == "__main__":
    from glyphNameFormatter.exporters import printRange
    printRange("Transport and Map Symbols")
