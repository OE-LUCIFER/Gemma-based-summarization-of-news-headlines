# this file defines a base summarizer class.

class Summarizer:
    def __init__(self):
        pass

    def summarize(self, text: str, max_length: int = 512):
        raise NotImplementedError
