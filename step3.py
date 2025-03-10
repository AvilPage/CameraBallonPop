import random

import numpy as np
import pygame
import cv2
from cvzone.HandTrackingModule import HandDetector

height, width = 480, 640

capture = cv2.VideoCapture(0)
capture.set(3, height)
capture.set(4, width)

def get_image_info():
    image_name = 'ballon.png'
    image = pygame.image.load(image_name).convert_alpha()
    image_rect = image.get_rect()

    # here we are declaring position of ballon (W, H)
    image_rect.x = random.randint(0, width)
    image_rect.y = height

    return image_name, image, image_rect


def main():
    window = pygame.display.set_mode((width, height))
    hand_detector = HandDetector(detectionCon=0.25, maxHands=2)

    image_name, img_ballon, rect_ballon = get_image_info()

    speed = 5

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

        # move ballon up
        rect_ballon.y -= speed

        # if ballon is out of screen, create new ballon
        if rect_ballon.y < 0:
            image_name, img_ballon, rect_ballon = get_image_info()

        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_rgb = np.rot90(img_rgb)
        frame = pygame.surfarray.make_surface(img_rgb).convert()

        window.blit(frame, (0, 0))

        # show ballon
        window.blit(img_ballon, rect_ballon)

        pygame.display.update()


if __name__ == "__main__":
    main()
