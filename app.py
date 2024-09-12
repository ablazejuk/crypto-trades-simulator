from dependencies import configure_injections
from gui import GUI
import inject
from singleton_metaclass import SingletonMeta

class App(metaclass=SingletonMeta):
    @inject.autoparams()
    def __init__(self, gui: GUI):
        self.gui = gui

    def main(self):
        self.gui.run()

if __name__ == "__main__":
    inject.configure(configure_injections)
    app = App()
    app.main()
