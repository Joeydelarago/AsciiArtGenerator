import sys
from PyQt5.QtWidgets import QApplication
from ascii_generator.gui.generator_window import GeneratorWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ascii_app = GeneratorWindow()
    ascii_app.show()
    sys.exit(app.exec_())
