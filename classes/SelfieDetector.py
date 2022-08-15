import mediapipe as mp
import cv2 as cv
import numpy as np
import imutils


class SelfieDetector:
    def __init__(self):
        self.mp_selfie = mp.solutions.selfie_segmentation
        self.selfie = self.mp_selfie.SelfieSegmentation(
            model_selection=1)
        self.bg_image = None
        self.bg_default = (192, 192, 192)

    def find_selfie(self, frame, image=None):
        img_color = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.selfie.process(img_color)

        _, th = cv.threshold(self.results.segmentation_mask,
                             0.75, 255, cv.THRESH_BINARY)
        th = th.astype(np.uint8)
        th = cv.medianBlur(th, 5)
        th_inv = cv.bitwise_not(th)

        if image is None:
            bg_image = np.ones(frame.shape, dtype=np.uint8)
            bg_image[:] = self.bg_default
        else:
            bg_image = cv.imread(image, 1)
            bg_image = cv.resize(bg_image, dsize=(640, 480))
            # bg_image = cv.cvtColor(bg_image, cv.COLOR_BGR2RGB)

        bg = cv.bitwise_and(bg_image, bg_image, mask=th_inv)

        fg = cv.bitwise_and(frame, frame, mask=th)

        output_image = cv.add(bg, fg)

        return output_image
