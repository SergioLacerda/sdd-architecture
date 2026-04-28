class Assertion:
    def __init__(self, **kwargs):
        self.params = kwargs

    def execute(self, context):
        raise NotImplementedError()
