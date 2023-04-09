import maya.cmds as cmds
import shiboken2
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtCore import Qt
import maya.OpenMayaUI as apiUI
import tempfile

import sys
if 'C:/Users/sunli/Documents/AutoMuse/sketch2pose-main/src' not in sys.path:
    sys.path.insert(0, 'C:/Users/sunli/Documents/AutoMuse/sketch2pose-main/src')

from AutoMuse import AutoMuse
autoMuse = AutoMuse(cmds)

class Canvas(QtWidgets.QLabel):

    def __init__(self):
        super().__init__()
        pixmap = QtGui.QPixmap(600, 300)
        pixmap.fill(Qt.white)
        self.setPixmap(pixmap)

        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor('#000000')

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)

    def mouseMoveEvent(self, e):
        if self.last_x is None: # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return # Ignore the first time.

        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(4)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None
        
COLORS = [
# 17 undertones https://lospec.com/palette-list/17undertones
'#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49',
'#458352', '#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b',
'#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
]


class QPaletteButton(QtWidgets.QPushButton):

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QtCore.QSize(24,24))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        
        self.canvas = Canvas()

        self.centralwidget = QtWidgets.QWidget(self)
        #self.resize(500, 500)
        
        
        layout = QtWidgets.QVBoxLayout()
        self.centralwidget.setLayout(layout)
        layout.addWidget(self.canvas)
        
        palette = QtWidgets.QHBoxLayout()
        self.add_palette_buttons(palette)
        layout.addLayout(palette)
        
        row2 = QtWidgets.QHBoxLayout()
        
        clearBtn = QtWidgets.QPushButton("Clear")
        row2.addWidget(clearBtn)
        loadImgBtn = QtWidgets.QPushButton("Load Image")
        row2.addWidget(loadImgBtn)
        genSkelBtn = QtWidgets.QPushButton("Generate Skeleton")
        genSkelBtn.clicked.connect(self.genSkeleton)
        row2.addWidget(genSkelBtn)
        replaceSkelBtn = QtWidgets.QPushButton("Replace Selected Skeleton")
        row2.addWidget(replaceSkelBtn)
                
        layout.addLayout(row2)
        
        row3 = QtWidgets.QHBoxLayout()
        
        animationLabel = QtWidgets.QLabel("Animation")
        row3.addWidget(animationLabel)
        loadImgsBtn = QtWidgets.QPushButton("Load Images")
        row3.addWidget(loadImgsBtn)        
        
        layout.addLayout(row3)
        
        row4 = QtWidgets.QHBoxLayout()
        
        scaleLabel = QtWidgets.QLabel("Skeleton Scale")
        row4.addWidget(scaleLabel)
        self.scaleSpinner = QtWidgets.QDoubleSpinBox()
        self.scaleSpinner.setRange(0.0, 20.0)
        self.scaleSpinner.setValue(5.0)
        row4.addWidget(self.scaleSpinner)
        meshLabel = QtWidgets.QLabel("Apply to mesh?")
        row4.addWidget(meshLabel)
        meshSelector = QtWidgets.QComboBox()
        row4.addWidget(meshSelector)        
        
        layout.addLayout(row4)
        
        """
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(380, 350, 75, 23))
        self.pushButton.clicked.connect(self.doMayaThing)
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.canvas = QtGui.QPixmap(400, 300)
        self.canvas.fill(Qt.white)
        self.label.setPixmap(self.canvas)
        """
        
        self.setCentralWidget(self.centralwidget)
        #self.menubar = QtWidgets.QMenuBar(self)
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        #self.setMenuBar(self.menubar)
        #self.statusbar = QtWidgets.QStatusBar(self)
        #self.setStatusBar(self.statusbar)
        #self.retranslateUi()
        #self.last_x, self.last_y = None, None
        #self.draw_something()

    def add_palette_buttons(self, layout):
        for c in COLORS:
            b = QPaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.set_pen_color(c))
            layout.addWidget(b)

    def retranslateUi(self):
        self.setWindowTitle("MainWindow")
        self.pushButton.setText("test")
        
        
    def genSkeleton(self):
        print(self.scaleSpinner.value())
        autoMuse.generate_single(None, scale=self.scaleSpinner.value())
        
    def mouseMoveEvent(self, e):
        if self.last_x is None: # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return # Ignore the first time.

        painter = QtGui.QPainter(self.label.pixmap())
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None
        
    def draw_something(self):
        from random import randint, choice
        colors = ['#FFD141', '#376F9F', '#0D1F2D', '#E9EBEF', '#EB5160']
    
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(3)
        painter.setPen(pen)
    
        for n in range(10000):
            # pen = painter.pen() you could get the active pen here
            pen.setColor(QtGui.QColor(choice(colors)))
            painter.setPen(pen)
            painter.drawPoint(
                200+randint(-100, 100),  # x
                150+randint(-100, 100)   # y
                )
        painter.end()




def getMayaWindow():
    """
    Get the main Maya window as a QtGui.QMainWindow instance
    @return: QtGui.QMainWindow instance of the top level Maya windows
    """
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken2.wrapInstance(int(ptr), QtWidgets.QWidget)

def mayaMain():
    global maya_basicTest_window
    try:
        maya_basicTest_window.close()
    except:
        pass
    maya_basicTest_window = Ui_MainWindow(getMayaWindow())
    maya_basicTest_window.show()

mayaMain()