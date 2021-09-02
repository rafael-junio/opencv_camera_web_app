import cv2
import numpy as np


class ImageProcess:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)

    @staticmethod
    def draw_retangle(frame, x, y, dx, dy, color=(0, 255, 0), thickness=1):
        drawed_frame = cv2.rectangle(frame, (x, y), (dx, dy), color=color, thickness=thickness)
        return drawed_frame

    @staticmethod
    def binarize(frame, r, g, b, k):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        binarized_frame = np.zeros((frame.shape[0], frame.shape[1]))
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                binarized_frame[i, j] = (frame[i, j, 0] * r + frame[i, j, 1] * g + frame[i, j, 0] * b) > k
        binarized_frame = np.where(binarized_frame == 1, 0, 255)
        return binarized_frame

    @staticmethod
    def get_masked_frame(frame, mask):
        mask = cv2.merge((mask, mask, mask))
        subtracted_frame = np.where(mask == 0, 0, frame)
        return subtracted_frame

    @staticmethod
    def extract_mask(frame, old_frame):
        mask = cv2.subtract(old_frame, frame)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        mask = np.where(mask < 25, 0, 255)
        return mask

    def get_detected_faces(self, cascade_classifier, frame):
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detected_faces = cascade_classifier.detectMultiScale(frame_gray, 1.2, 6)
        for x, y, w, h in detected_faces:
            frame = self.draw_retangle(frame, x, y, x + w, y + h, thickness=2)
        return frame

    @staticmethod
    def encode_frame(frame):
        ret, buffer = cv2.imencode('.jpg', frame)
        encoded_frame = buffer.tobytes()
        return encoded_frame

    def get_frame(self):
        _, frame = self.camera.read()
        return _, frame

    def stream(self, frame, fps):
        self.draw_label(frame, f'Tamanho: {frame.shape}, FPS: {fps:.2f}')
        encoded_frame = self.encode_frame(frame)
        return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + encoded_frame + b'\r\n\r\n'

    @staticmethod
    def draw_label(frame, label, color=(0, 0, 0)):
        image_h, image_w, _ = frame.shape
        position = (5, image_h - 5)
        label_thickness = int(0.6 * (image_h + image_w) / 1000)
        (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1,
                                                              thickness=label_thickness)
        x1, y1 = position
        p2 = (x1 + text_width, y1 - text_height - baseline)

        cv2.rectangle(frame, position, p2, color=color, thickness=cv2.FILLED)
        cv2.putText(frame, label, (x1, y1 - 4), cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1,
                    color=(255, 255, 255), thickness=label_thickness, lineType=cv2.LINE_AA)
