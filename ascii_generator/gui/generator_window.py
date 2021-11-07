from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QBoxLayout, QCheckBox, QColorDialog,
                             QDialog, QFileDialog, QGridLayout, QGroupBox, QLabel, QPushButton, QVBoxLayout)

from ascii_generator.ascii_generator.grayscale_ascii_generator import AsciiImageGenerator


class GeneratorWindow(QDialog):
    def __init__(self, parent=None):
        super(GeneratorWindow, self).__init__(parent)

        self.asciiImageGenerator = AsciiImageGenerator()
        self.bg_color = ""
        self.font_color = ""

        self.originalPalette = QApplication.palette()

        self.createLeftGroup()
        self.createRightGroup()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.leftGroup, 0, 0)
        mainLayout.addWidget(self.rightGroup, 0, 1)

        self.setLayout(mainLayout)

        self.setMinimumWidth(640)
        self.setMinimumHeight(520)

    def createRightGroup(self):
        self.rightGroup = QGroupBox("Right Group")

        self.image_label = QLabel("")
        pixmap = QtGui.QPixmap("")
        self.image_label.setPixmap(pixmap)
        self.image_label.setMinimumWidth(400)
        self.image_label.setMinimumHeight(400)

        loadImageButton = QPushButton("Load Image")
        loadImageButton.clicked.connect(self.load_image)

        saveImageButton = QPushButton("Save Image")
        saveImageButton.clicked.connect(self.save_image)

        copyAsciiButton = QPushButton("Copy Ascii")
        copyAsciiButton.clicked.connect(self.copy_ascii)

        generateImageButton = QPushButton("Generate Image")
        generateImageButton.clicked.connect(self.generate_image)

        topLayout = QVBoxLayout()

        bottomLayout = QVBoxLayout()
        bottomLayout.setDirection(QBoxLayout.LeftToRight)

        outerLayout = QVBoxLayout()
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(bottomLayout)

        topLayout.addWidget(self.image_label)

        bottomLayout.addWidget(loadImageButton)
        bottomLayout.addWidget(saveImageButton)
        bottomLayout.addWidget(copyAsciiButton)
        bottomLayout.addWidget(generateImageButton)

        self.rightGroup.setLayout(outerLayout)

    def createLeftGroup(self):
        self.leftGroup = QGroupBox("Left Group")

        checkBox = QCheckBox("Dynamic Text Color")
        checkBox.setChecked(False)

        bgColorButton = QPushButton("Background Color")
        bgColorButton.pressed.connect(
            lambda: self.set_bg_color(self.color_picker(self.bg_color)))

        fontColorButton = QPushButton("Font Color")
        fontColorButton.pressed.connect(
            lambda: self.set_font_color(self.color_picker(self.font_color)))

        dynamicTextCheckBox = QCheckBox("Dynamic Color")
        dynamicTextCheckBox.toggled.connect(lambda: self.update_dynamic_text(
            dynamicTextCheckBox.isChecked(), fontColorButton))

        layout = QVBoxLayout()
        layout.addWidget(dynamicTextCheckBox)
        layout.addWidget(bgColorButton)
        layout.addWidget(fontColorButton)

        layout.addStretch()

        self.leftGroup.setLayout(layout)

    def generate_image(self):
        if (self.asciiImageGenerator.input_image):
            image_name = self.asciiImageGenerator.create_ascii_image()
            self.update_image(image_name)

    def load_image(self):
        input_image_name, _ = QFileDialog.getOpenFileName(
            self, 'Open file', '.', "Image files (*.jpg *.gif *.png)")

        if input_image_name:
            self.asciiImageGenerator.set_input_image(input_image_name)
            self.update_image(input_image_name)

    def update_image(self, image_name: str):
        pixmap = QtGui.QPixmap(image_name)

        pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)

        self.image_label.setPixmap(pixmap)

    def save_image(self):
        print("save")

    def copy_ascii(self):
        print("copy ascii")

    def color_picker(self, color):
        dlg = QtWidgets.QColorDialog(self)
        if color:
            dlg.setCurrentColor(QtGui.QColor(color))

        if dlg.exec_():
            return dlg.currentColor().name()

    def update_dynamic_text(self, state, fontColorButton):
        fontColorButton.setEnabled(not state)

    def set_bg_color(self, bg_color):
        self.bg_color = bg_color

    def set_font_color(self, font_color):
        self.font_color = font_color
