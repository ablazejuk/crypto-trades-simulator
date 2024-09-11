from dependencies import configure_injections
from gui import GUI
import inject

class App:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    @inject.autoparams()
    def __init__(self, gui: GUI):
        if not self.__initialized:
            self.gui = gui
            self.__initialized = True

    def main(self):
        self.gui.run()

if __name__ == "__main__":
    inject.configure(configure_injections)
    app = App()
    app.main()
