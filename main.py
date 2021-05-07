'''
Main file for the Space Invader Game
Using pygame Module
'''

import pygame
from pygame import mixer
import random
import math

# initialize pygame
pygame.init()

# to create a screen
screen = pygame.display.set_mode((800, 600))
mixer.music.load('background_music.wav')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
background = pygame.image.load('background.png')

# player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# enemy
target = pygame.image.load('target.png')
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 5

# for multiple enemies
for i in range(num_enemies):
    enemyImg.append(target)
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 100))
    enemyX_change.append(3)
    enemyY_change.append(20)

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = False

# score
score_value = 0
font = pygame.font.Font('scoreboard.ttf', 32)
textX = 10
textY = 10

# lives
life = pygame.image.load('life.png')
lifeX = []
lifeY = []
X = 800
num_lives = 3

for i in range(num_lives):
    lifeX.append(X - 42)
    lifeY.append(5)
    X -= 42

# level up
alien = pygame.image.load('alien.png')


# function to draw the player on screen
def player(x, y):
    screen.blit(playerImg, (x, y))


# function to draw enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# function to fire bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = True
    screen.blit(bulletImg, (x + 16, y + 16))


# function for collision detection
def isCollision(x1, y1, x2, y2):
    dist = math.sqrt((math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2)))
    if dist < 27:
        return True
    return False


# function to display score
def showScore(x, y):
    score = font.render("Score:{}".format(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


# function to display lives
def lives(x, y):
    screen.blit(life, (x, y))


# game over function
def game_over():
    newFont = pygame.font.Font('scoreboard.ttf', 64)
    text = newFont.render("GAME OVER".format(score_value), True, (255, 0, 0))
    screen.blit(text, (250, 250))


# game loop
running = True
while running:

    # adding screen color
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # loop through all the events and if quit  event is triggered then break the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_UP:
                playerY_change = -5
            if event.key == pygame.K_DOWN:
                playerY_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is False:
                    bullet_sound = mixer.Sound('bullet_shot.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        # when key is released then set changes to 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # to add boundaries on x-axis
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # to add boundaries on y-axis
    playerY += playerY_change
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # for enemy boundaries and movement
    for i in range(num_enemies):

        # game over
        if enemyY[i] > 480:
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over_sound = mixer.Sound('game_over.wav')
            game_over_sound.play()
            mixer.music.pause()
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # bullet collision
        collisionBullet = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collisionBullet:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()

            # reset the bullet and reset the enemy
            bulletY = playerY
            bullet_state = False

            # if alien is hit then change it to target
            if enemyImg[i] == alien:
                enemyImg[i] = target
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            score_value += 1

            if score_value % 5 == 0 and score_value != 0:
                # for multiple enemies
                for k in range(3):
                    enemyImg.append(alien)
                    enemyX.append(random.randint(0, 736))
                    enemyY.append(random.randint(50, 100))
                    enemyX_change.append(6)
                    enemyY_change.append(30)

                    levelUp_sound = mixer.Sound('level_up.wav')
                    levelUp_sound.play()

                num_enemies += 3

        # function calling
        enemy(enemyX[i], enemyY[i], i)

    # for lives to display
    for i in range(num_lives):
        lives(lifeX[i], lifeY[i])

        # player collision detection
        for j in range(num_enemies):
            collisionPlayer = isCollision(enemyX[j], enemyY[j], playerX, playerY)
            if collisionPlayer:
                player_collision = mixer.Sound('player_collision.wav')
                player_collision.play()
                playerX = 370
                playerY = 480
                num_lives -= 1

                # game over by lives
                if num_lives == 0:
                    for j in range(num_enemies):
                        enemyY[j] = 2000
                    game_over_sound = mixer.Sound('game_over.wav')
                    game_over_sound.play()
                    mixer.music.pause()
                    game_over()
                    break

    # bullet movement
    if bulletY <= 0:
        bullet_state = False
        bulletY = playerY
    if bullet_state is True:
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # function calling to draw player and score board
    player(playerX, playerY)
    showScore(textX, textY)

    # update screen
    pygame.display.update()

