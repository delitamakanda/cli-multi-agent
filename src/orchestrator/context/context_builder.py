class ContextBuilder:
    def __init__(self):
        self._context = {}

    def set(self, key, value):
        self._context[key] = value
        return self

    def build(self):
        return self._context