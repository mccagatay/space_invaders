import pygame as py
import random
import math

from pygame import mixer

# pencereyi calistiran komut
py.init()

# ekran boyutu
screen = py.display.set_mode((800, 600))

# pencere basligi
py.display.set_caption("Space İnvaders")

# pencerenin ikonu
icon = py.image.load('ufo.jpg')
py.display.set_icon(icon)

background = py.image.load('background.jpg')

mixer.music.load('background.wav')
mixer.music.play(-1)

playerImg = py.image.load('spaceship.png')
playerX = 170
playerY = 380
playerX_change = 0
playerY_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(py.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(20)

bulletImg = py.image.load('bullet.png')
bulletX = random.randint(0, 736)
bulletY = 380
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

score_value = 0
font = py.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

over_font = py.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (220, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0,))
    screen.blit(background, (0, 0))

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        # pencerenin arkaplan rengi
        if event.type == py.KEYDOWN:
            print("A keystoke is pressed")
            if event.key == py.K_LEFT:
                playerX_change = -2

            if event.key == py.K_RIGHT:
                playerX_change = 2

            if event.key == py.K_SPACE:
                if bulletY == playerY:
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == py.KEYUP:
            if event.key == py.K_LEFT or event.key == py.K_RIGHT:
                playerX_change = 0
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    for i in range(num_of_enemies):
        if enemyY[i] > 200:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            print(score_value)
        enemy(enemyX[i], enemyY[i], i)
    player(playerX, playerY)
    show_score(textX, textY)
    py.display.update()
