class MoveLog:
    def __init__(self, tag, card=None, dest=None, source=None, flip=False):
        self.tag = tag
        self.card = card
        self.dest = dest
        self.source = source
        self.flip = flip
