# import
import os
import time

import pygame
import cv2
import numpy as np  # control matrices
import random
from cvzone.HandTrackingModule import HandDetector

# initialize
pygame.init()

# Create Window
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("AvilPage - CV Ballon Pop Game")

# Intialize Clock for FPS
fps = 30
clock = pygame.time.Clock()

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # height
cap.set(4, 720)  # width

# Images
# imgBallon = pygame.image.load("BalloonRed.png").convert_alpha()
# rectBallon = imgBallon.get_rect()

def get_target_image():
    targets = os.listdir('targets')
    target_images = [target for target in targets if target.endswith('.png')]
    target_image_name = random.choice(target_images)
    target_image = pygame.image.load(f'targets/{target_image_name}').convert_alpha()
    target_rect = target_image.get_rect()
    return target_image_name, target_image, target_rect

target_image_name, imgBallon, rectBallon = get_target_image()
rectBallon.x, rectBallon.y = 500, 300  # here we are declaring postion of ballon (W,H)

# variables
total_speed = 0
speed = 5
score = 0
missed = 0

# Hand Detector
detector = HandDetector(detectionCon=0.3, maxHands=2)
# use mirrored video


def resetBallon(audio=None):
    global target_image_name, rectBallon, imgBallon
    print(target_image_name)

    splash = pygame.image.load("splash.png").convert_alpha()
    window.blit(imgBallon, splash.get_rect())

    # play sound
    if not audio:
        audio = "blast.mp3"
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play()

    target_image_name, imgBallon, rectBallon = get_target_image()

    rectBallon.x = random.randint(100, img.shape[1] - 100)
    rectBallon.y = img.shape[0] + 50


# main loop
start = True
while start:
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # apply logic

    # openCV
    success, img = cap.read()

    # flip video
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, flipType=True)
    img = cv2.flip(img, 1)

    total_speed = speed + score // 3
    rectBallon.y -= total_speed  # move the ballon up r

    # We are adding this becuase as soon as ballon reach to the top of window it should be reset
    if rectBallon.y < 0:
        missed += 1
        if missed >= 3:
            # show game over
            textScore = font.render(f"GAME OVER", True, (255, 50, 50))
            window.blit(textScore, (500, 500))

            textScore = font.render(f"Your Score: {score}", True, (255, 50, 50))
            window.blit(textScore, (500, 550))

            pygame.display.update()

            time.sleep(5)
            start = False
            print("Game Over")

        resetBallon(audio="laugh.mp3")
        speed += 3

    if hands:
        for hand in hands:
            x = hand['lmList'][8][0]
            y = hand['lmList'][8][1]

            if rectBallon.collidepoint(x, y):
                resetBallon()
                score += 1
                break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # we did this because CV use BRG convention and pygame use RGB so we converted
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    # frame = pygame.transform.flip(frame,True,False)
    window.blit(frame, (0, 0))
    window.blit(imgBallon, rectBallon)

    font = pygame.font.Font("text.ttf", 50)
    textScore = font.render(f"Score :{score}", True, (255, 50, 50))
    window.blit(textScore, (35, 0))

    textScore = font.render(f"Speed :{total_speed}", True, (255, 50, 50))
    window.blit(textScore, (35, 50))

    textScore = font.render(f"Missed :{missed}", True, (255, 50, 50))
    window.blit(textScore, (35, 100))

    # Update Display/Window
    pygame.display.update()

    # set FPs
    clock.tick(fps)
