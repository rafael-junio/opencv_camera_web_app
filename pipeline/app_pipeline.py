import cv2
import numpy as np


class AppPipeline:

    def __init__(self):
        self.__open_camera()
        self.background = None

    def __get_frame(self):
        _, frame = self.camera.read()
        return _, frame

    def stream(self):
        while True:
            _, frame = self.__get_frame()
            ret, buffer = cv2.imencode('.jpg', frame)
            encoded_frame = buffer.tobytes()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + encoded_frame + b'\r\n\r\n'

    def __open_camera(self):
        self.camera = cv2.VideoCapture(0)

    def background_subtract(self):
        old_frame = self.background
        while True:
            _, frame = self.__get_frame()
            mask = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            subtracted_frame = cv2.subtract(old_frame, frame, mask=mask)
            ret, buffer = cv2.imencode('.jpg', subtracted_frame)
            encoded_frame = buffer.tobytes()
            if self.background is not None:
                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + encoded_frame + b'\r\n\r\n'
            else:
                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + b'\r\n\r\n'

    def set_background(self):
        _, self.background = self.__get_frame()
