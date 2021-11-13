from typing import Tuple
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
        self.rightGroup = QGroupBox()

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

        self.rightGroup.setLayout(outerLayout)

    def createLeftGroup(self):
        self.leftGroup = QGroupBox()

        bgColorButton = QPushButton("Background Color")
        bgColorButton.pressed.connect(self.set_bg_color)

        fontColorButton = QPushButton("Font Color")
        fontColorButton.pressed.connect(self.set_font_color)

        dynamicTextColorCheckBox = QCheckBox("Dynamic Font Color")
        dynamicTextColorCheckBox.toggled.connect(lambda: self.set_dynamic_color(dynamicTextColorCheckBox.isChecked(), fontColorButton))

        layout = QVBoxLayout()
        layout.addWidget(bgColorButton)
        layout.addWidget(dynamicTextColorCheckBox)
        layout.addWidget(fontColorButton)

        layout.addStretch()

        self.leftGroup.setLayout(layout)

    def generate_image(self):
        if (self.asciiImageGenerator.input_image):
            image_name = self.asciiImageGenerator.create_ascii_image()
            self.update_image(image_name)

    def update_image(self, image_name: str):
        pixmap = QtGui.QPixmap(image_name)

        pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)

        self.image_label.setPixmap(pixmap)


    def load_image(self):
        input_image_name, _ = QFileDialog.getOpenFileName(
            self, 'Open file', '.', "Image files (*.jpg *.gif *.png)")

        if (input_image_name):
            self.asciiImageGenerator.set_input_image(input_image_name)
            self.update_image(input_image_name)
            self.generate_image()

    def save_image(self):
        output_image_name, _ = QFileDialog.getSaveFileName(self, 'Save File')
        
        if (output_image_name):
            self.asciiImageGenerator.save_image(output_image_name)

    def copy_ascii(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.asciiImageGenerator.get_ascii_text(), mode=cb.Clipboard)

    def color_picker(self, color):
        dlg = QtWidgets.QColorDialog(self)
        if color:
            dlg.setCurrentColor(QtGui.QColor.toRgb(color))

        if dlg.exec_():
            return dlg.currentColor()

    def set_bg_color(self):
        bg_color = self.color_picker(self.bg_color)
        if (bg_color):
            self.bg_color = bg_color
            self.asciiImageGenerator.set_background_color(bg_color.getRgb())
            self.generate_image()

    def set_font_color(self):
        font_color = self.color_picker(self.font_color)
        if (font_color):
            self.font_color = font_color
            self.asciiImageGenerator.set_font_color(font_color.getRgb())
            self.generate_image()
        
    def set_dynamic_color(self, dynamic_color: bool, fontColorButton: QPushButton):
        fontColorButton.setEnabled(not dynamic_color)
        self.asciiImageGenerator.set_dynamic_color(dynamic_color)
        self.generate_image()
