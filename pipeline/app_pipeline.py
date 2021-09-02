import time
import cv2
from pipeline.image_process import ImageProcess


class AppPipeline(ImageProcess):

    def __init__(self):
        super().__init__()
        self.background = None

    def background_frame(self):
        old_frame = self.background
        while True:
            fps_start = time.time()
            _, frame = self.get_frame()
            mask = self.extract_mask(frame, old_frame)
            subtracted_frame = self.get_masked_frame(frame, mask)
            fps_end = 1.0 / (time.time() - fps_start)
            if self.background is not None:
                yield self.stream(subtracted_frame, fps_end)

    def camera_render(self):
        while True:
            fps_start = time.time()
            _, frame = self.get_frame()
            fps_end = 1.0 / (time.time() - fps_start)
            yield self.stream(frame, fps_end)

    def binarize_render(self):
        while True:
            fps_start = time.time()
            _, frame = self.get_frame()
            binarized_frame = self.get_binary_frame(frame)
            fps_end = 1.0 / (time.time() - fps_start)
            yield self.stream(binarized_frame, fps_end)

    def get_binary_frame(self, frame):
        binarized_frame = self.binarize(frame, self.r, self.g, self.b, self.k)
        binarized_frame = cv2.merge((binarized_frame, binarized_frame, binarized_frame))
        return binarized_frame

    def detect_faces_render(self):
        cascade_classifier = cv2.CascadeClassifier('pipeline/models/haarcascade_frontalface_default.xml')
        while True:
            fps_start = time.time()
            _, frame = self.get_frame()
            frame = self.get_detected_faces(cascade_classifier, frame)
            fps_end = 1.0 / (time.time() - fps_start)
            yield self.stream(frame, fps_end)

    def set_background(self):
        _, self.background = self.get_frame()

    def crop_image(self):
        _, frame = self.get_frame()
        self.cache_cropped_image(frame)
        marked_image = self.draw_retangle(frame, self.x, self.y, self.dx, self.dy)
        return self.stream(marked_image, 0)

    def cache_cropped_image(self, frame):
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
