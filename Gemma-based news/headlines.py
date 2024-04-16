# this file provides a base class for news headline restrieval.

class Headlines:
    def __init__(self):
        pass

    def get_headlines(self, query: str = None, max_headlines: int = 10):
        raise NotImplementedError
