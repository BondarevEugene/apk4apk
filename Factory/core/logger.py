class Logger:

    def __init__(self, app):
        self.app = app

    def log(self, text):

        print(text)

        self.app.log(text)