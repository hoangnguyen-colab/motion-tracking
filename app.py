# library
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import cv2
from main_window import *
import cv2
import numpy as np

# variable
min_contour_width = 40  # 40
min_contour_height = 40  # 40
offset = 10  # 10
line_height = 530  # 530
matches = []
cars = 0
motors = 0
car_desire_length = 100
scale_percent = 50


def get_center(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1
    return cx, cy

def process_img(frame1, frame2):
    global cars, motors
    img = frame1
    d = cv2.absdiff(img, frame2)
    grey = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (5, 5), 0)
    ret, th = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(th, np.ones((3, 3)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))

    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    contours, h = cv2.findContours(
        closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for(i, c) in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(c)
        contour_valid = (w >= min_contour_width) and (h >= min_contour_height)

        if not contour_valid:
            continue
        cv2.rectangle(img, (x-10, y-10), (x+w+10, y+h+10), (255, 0, 0), 2)
        cv2.line(img, (0, line_height), (1200, line_height), (0, 255, 0), 2)

        center = get_center(x, y, w, h)
        matches.append(center)
        cv2.circle(img, center, 5, (0, 255, 0), -1)
        cx, cy = get_center(x, y, w, h)

        for (x, y) in matches:
            if y < (line_height+offset) and y > (line_height-offset):
                if w > car_desire_length:
                    cars = cars+1
                else:
                    motors = motors+1

                matches.remove((x, y))

    cv2.putText(img, "Cars: " + str(cars), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 170, 0), 2)
    cv2.putText(img, "Motors: " + str(motors), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 170, 0), 2)

    img, frame2 = resize(img, frame2)
    return img, frame2

def resize(frame1, frame2):
    # resize
    width = int(frame1.shape[1] * scale_percent / 100)
    height = int(frame1.shape[0] * scale_percent / 100)
    frame1_sz = cv2.resize(frame1, (width, height),
                           interpolation=cv2.INTER_AREA)
    frame2_sz = cv2.resize(frame2, (width, height),
                           interpolation=cv2.INTER_AREA)

    return frame1_sz, frame2_sz

class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        super().__init__()
        self.filePath = ""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.timer = QTimer()
        self.timer.timeout.connect(self.view_video)
        self.ui.control_btn.clicked.connect(self.button_start)
        self.ui.file_load_btn.clicked.connect(self.openFileNameDialog)

    # view camera
    def view_video(self):
        frame1 = self.frame1
        frame2 = self.frame2
        proc, origin = process_img(frame1, frame2)

        proc = cv2.cvtColor(proc, cv2.COLOR_BGR2RGB)
        origin = cv2.cvtColor(origin, cv2.COLOR_BGR2RGB)

        # create QImage from image
        height, width, channel = proc.shape
        step = channel * width
        qImg_procvid = QImage(proc.data, width, height,
                              step, QImage.Format_RGB888)

        self.ui.process_vid.setPixmap(QPixmap.fromImage(qImg_procvid))

        self.frame1 = self.frame2
        _, self.frame2 = self.cap.read()

    # start/stop timer
    def button_start(self):
        # check path null
        if not self.filePath:
            self.messageBox()
        else:
            # if timer is stopped
            if not self.timer.isActive():
                self.cap = cv2.VideoCapture('traffic.mp4')
                _, self.frame1 = self.cap.read()
                _, self.frame2 = self.cap.read()

                self.timer.start(1)
                self.ui.control_btn.setText("Stop")

            # if timer is started
            else:
                self.timer.stop()
                self.cap.release()
                self.ui.control_btn.setText("Start")

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Open video file", "", "All Files (*);;Video Files (*.mp4)", options=options)
        if filePath:
            self.filePath = filePath

    def messageBox(self):
        buttonReply = QMessageBox.question(self, 'Path is empty!', "Please open mp4 file first...", QMessageBox.Cancel)
        # if buttonReply == QMessageBox.Cancel:
        #     print('Yes clicked.')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
