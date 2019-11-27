import pygame
import random
import math


pygame.init()
clock = pygame.time.Clock()


score_value = 0
font = pygame.font.Font('freesansbold.ttf', 20)
textX = 10
textY = 10

screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.png')


pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_enemies = 6

for i in range(num_enemies):

    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(64, 180))
    enemyX_change.append(2)
    enemyY_change.append(40)

for i in range(2):
    x = random.randint(0, 2)
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyImg.append(pygame.image.load('enemy2.png'))
    enemyImg.append(pygame.image.load('enemy3.png'))

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# explosion
explosionImg = pygame.image.load("explosion.png")

font2 = pygame.font.Font('freesansbold.ttf', 80)


def explosion(img):
    exp = img
    img = explosionImg
    screen.blit(img, (enemyX[i], enemyY[i]))
    pygame.time.delay(100)
    img = exp


def game_over():
    disp = font2.render("GAME OVER!!", True, (255, 255, 255))
    screen.blit(disp, (150, 250))


def score(x, y):
    score = font.render("SCORE:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) +
                         (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# gameloop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_UP:
                playerY_change = -3
            if event.key == pygame.K_DOWN:
                playerY_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
    playerX += playerX_change
    playerY += playerY_change
    if (playerX <= 0):
        playerX = 0
    if (playerX >= 736):
        playerX = 736
    if (playerY <= 0):
        playerY = 0
    if (playerY >= 536):
        playerY = 536

    for i in range(num_enemies):

        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over()
            break
        enemyX[i] += enemyX_change[i]
        if (enemyX[i] >= 736):
            enemyY[i] += enemyY_change[i]
            enemyX[i] = 736
            enemyX_change[i] = -enemyX_change[i]
        if (enemyX[i] <= 0):
            enemyY[i] += enemyY_change[i]
            enemyX[i] = 0
            enemyX_change[i] = 2

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            explosion(enemyImg[i])
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(64, 130)
        enemy(enemyX[i], enemyY[i], i)
        collision = isCollision(enemyX[i], enemyY[i], playerX, playerY)
        if collision:
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over()
            playerImg = explosionImg
            break

    if (bulletY <= 36):
        bullet_state = "ready"
        bulletY = 480
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    score(textX, textY)
    pygame.display.update()
