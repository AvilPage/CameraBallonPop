import random

import numpy as np
import pygame
import cv2
from cvzone.HandTrackingModule import HandDetector

height, width = 480, 640

capture = cv2.VideoCapture(0)
capture.set(3, height)
capture.set(4, width)


def main():
    window = pygame.display.set_mode((width, height))
    hand_detector = HandDetector(detectionCon=0.25, maxHands=2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        success, image = capture.read()
        image = cv2.flip(image, 1)
        hands, image = hand_detector.findHands(image, flipType=False)
        image = cv2.flip(image, 1)

        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_rgb = np.rot90(img_rgb)
        frame = pygame.surfarray.make_surface(img_rgb).convert()

        window.blit(frame, (0, 0))

        # img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # img_rgb = np.rot90(img_rgb)
        # frame = pygame.surfarray.make_surface(img_rgb).convert()

        # window.blit(frame, (0, 0))

        pygame.display.update()


if __name__ == "__main__":
    main()
