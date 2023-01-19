class BaseCommand:
    def __init__(self, argv: list = None):
        self.argv = argv

    def execute(self):
        pass
