# import
import os
import time
import datetime as dt

import pygame
import cv2
import numpy as np  # control matrices
import random
from cvzone.HandTrackingModule import HandDetector

# settings
FONT_LEFT_MARGIN = 10
FONT_COLOR = (255, 50, 50)

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
speed = 10
score = 0
missed = 0

# Hand Detector
detector = HandDetector(detectionCon=0.3, maxHands=2)
# use mirrored video


def resetBallon(audio=None):
    global target_image_name, rectBallon, imgBallon

    splash = pygame.image.load("splash.png").convert_alpha()
    window.blit(imgBallon, splash.get_rect())

    # play sound
    if audio:
        pygame.mixer.music.load(audio)
        pygame.mixer.music.play()

    target_image_name, imgBallon, rectBallon = get_target_image()

    rectBallon.x = random.randint(100, img.shape[1] - 100)
    rectBallon.y = img.shape[0] + 50


# main loop
start = True
start_timer = 10

is_timer_running = True
now = dt.datetime.now()
stop_time = now + dt.timedelta(seconds=start_timer)

while start:
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # openCV
    success, img = cap.read()

    # flip video
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    img = cv2.flip(img, 1)

    # show game timer for starting the game
    if is_timer_running:
        start_timer = int((stop_time - dt.datetime.now()).seconds) + 1
        font = pygame.font.Font("text.ttf", 50)
        textScore = font.render(f"Game Starting in {start_timer} seconds", True, FONT_COLOR)
        window.blit(textScore, (300, 300))
        pygame.display.update()
        clock.tick(fps)
        # time.sleep(0.1)
        is_timer_running = dt.datetime.now() < stop_time

    total_speed = speed + score // 3
    rectBallon.y -= total_speed  # move the ballon up r

    # We are adding this because as soon as ballon reach to the top of window it should be reset
    if not is_timer_running and rectBallon.y < 0:
        missed += 1
        if missed >= 3:
            # show game over
            textScore = font.render(f"GAME OVER", True, FONT_COLOR)
            window.blit(textScore, (500, 500))

            textScore = font.render(f"Your Score: {score}", True, FONT_COLOR)
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
                resetBallon(audio='blast.mp3')
                score += 1
                break

    # we did this because CV use BRG convention and pygame use RGB so we converted
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()

    window.blit(frame, (0, 0))
    window.blit(imgBallon, rectBallon)

    font = pygame.font.Font("text.ttf", 50)
    textScore = font.render(f"Score :{score}", True, FONT_COLOR)
    window.blit(textScore, (FONT_LEFT_MARGIN, 0))

    textScore = font.render(f"Speed :{total_speed}", True, FONT_COLOR)
    window.blit(textScore, (FONT_LEFT_MARGIN, 50))

    textScore = font.render(f"Missed :{missed}", True, FONT_COLOR)
    window.blit(textScore, (FONT_LEFT_MARGIN, 100))

    # Update Display/Window
    pygame.display.update()

    # set FPs
    clock.tick(fps)
