import cv2
import numpy as np


class AppPipeline:

    def __init__(self):
        self.__open_camera()
        self.background = None

    def background_subtract(self):
        old_frame = self.background
        while True:
            _, frame = self.__get_frame()
            mask = self.__extract_mask(frame, old_frame)
            mask = cv2.merge((mask, mask, mask))
            subtracted_frame = np.where(mask == 0, 0, frame)
            if self.background is not None:
                yield self.__stream(subtracted_frame)
            # else:
            #     yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + b'\r\n\r\n'

    def camera_render(self):
        while True:
            _, frame = self.__get_frame()
            yield self.__stream(frame)

    def binarize_frame(self):
        while True:
            _, frame = self.__get_frame()
            binarized_frame = self.__binarize(frame, self.r, self.g, self.b, self.k)
            yield self.__stream(binarized_frame)

    def set_background(self):
        _, self.background = self.__get_frame()

    def detect_faces(self):
        cascade_classifier = cv2.CascadeClassifier('pipeline/models/haarcascade_frontalface_default.xml')
        while True:
            _, frame = self.__get_frame()
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detected_faces = cascade_classifier.detectMultiScale(frame_gray, 1.2, 6)
            for x, y, w, h in detected_faces:
                frame = self.__draw_retangle(frame, x, y, x+w, y+h, thickness=2)
            yield self.__stream(frame)

    def crop_image(self):
        _, frame = self.__get_frame()
        self.__cache_cropped_image(frame)
        marked_image = self.__draw_retangle(frame, self.x, self.y, self.dx, self.dy)
        return self.__stream(marked_image)

    def __draw_retangle(self, frame, x, y, dx, dy, color=(0, 255, 0), thickness=1):
        drawed_frame = cv2.rectangle(frame, (x, y), (dx, dy), color=color, thickness=thickness)
        return drawed_frame

    def __cache_cropped_image(self, frame):
        frame = frame[self.y:self.dy, self.x:self.dx]
        cv2.imwrite('assets/cropped_image.jpg', frame)

    def set_crop_values(self, x, y, dx, dy):
        self.x = int(x)
        self.y = int(y)
        self.dx = int(dx)
        self.dy = int(dy)

    def set_binarize_values(self, r=1, g=1, b=1, k=328):
        self.r = r
        self.g = g
        self.b = b
        self.k = k

    @staticmethod
    def __binarize(frame, r, g, b, k):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        binarized_frame = np.zeros((frame.shape[0], frame.shape[1]))
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                binarized_frame[i, j] = (frame[i, j, 0] * r + frame[i, j, 1] * g + frame[i, j, 0] * b) > k
        binarized_frame = np.where(binarized_frame == 1, 0, 255)
        return binarized_frame

    @staticmethod
    def __extract_mask(frame, old_frame):
        mask = cv2.subtract(old_frame, frame)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        mask = np.where(mask < 25, 0, 255)
        return mask

    @staticmethod
    def __encode_frame(frame):
        ret, buffer = cv2.imencode('.jpg', frame)
        encoded_frame = buffer.tobytes()
        return encoded_frame

    def __open_camera(self):
        self.camera = cv2.VideoCapture(0)

    def __get_frame(self):
        _, frame = self.camera.read()
        return _, frame

    def __stream(self, frame):
        encoded_frame = self.__encode_frame(frame)
        return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + encoded_frame + b'\r\n\r\n'
