
def process(self):
    self.edit("HANGUL")
    self.edit("CHOSEONG", "choseong")
    self.edit("JONGSEONG", "jongseong")
    self.edit("JUNGSEONG", "jungseong")
    self.lower()
    self.replace("o-e", "o_e")  # ?
    self.replace("-")
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from glyphNameFormatter.test import printRange
    printRange("Hangul Jamo")
