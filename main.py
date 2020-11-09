import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()


# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
backgroundImg = pygame.image.load("background.jpg")

# Background music
mixer.music.load("background.wav")
mixer.music.play(-1)


# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)


# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_speed = 2
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))# so that the enemy respaws in random places
    enemyY.append(random.randint(50, 150))# so that the enemy respaws in random places
    enemyX_change.append(enemy_speed)
    enemyY_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Check collision between bullet and enemy
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Score
score_value = 0
font = pygame.font.Font("pixeled.ttf", 20)# create a font object
textX = 10# x coordinate of the font where we want it to appear
textY = 2# y coordinate of the font where we want it to appear

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Game Over Text
over_font = pygame.font.Font("pixeled.ttf", 64)# create a font object

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (135, 250))

# Game Loop
running = True
while running:
    # Set background color of screen
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(backgroundImg, (0,0))

    # Looping through all the events happening in the window
    for event in pygame.event.get():
        # Quit the game when window's cross icon is clicked
        if event.type == pygame.QUIT:
            running = False
    
        # if keystroke is pressed check whether its right or left or space
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")# plays bullet sound
                    bullet_sound.play()# plays bullet sound
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    
    # player movement mechanism
    # playerY -= 0.1

    # PLAYER MOVEMENT MECHANISM
    playerX += playerX_change

    # left and Right Boundary check of player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    # ENEMY MOVEMENT MECHANISM
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        # left and Right Boundary check of enemy
        if enemyX[i] <= 0:
            enemyX_change[i] = enemy_speed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -enemy_speed
            enemyY[i] += enemyY_change[i]
        
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")# plays explosion sound
            explosion_sound.play()# plays explosion sound
            bulletY = 480# reset bullet position
            bullet_state = "ready"# reset bullet state
            score_value += 1
            # increase enemy speed
            if score_value%10 == 0:
                enemy_speed += 0.5
            enemyX[i] = random.randint(0, 735)# respawn enemy
            enemyY[i] = random.randint(50, 150)# respawn enemy
        
        # call to enemy function
        enemy(enemyX[i], enemyY[i], i)
    
    # BULLET MOVEMENT MECHANISM
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    

    # call to player function
    player(playerX, playerY)# call after screen.fill so that the player remains above the screen background

    show_score(textX, textY)# call to show_score function to persist the updated score on the screen

    pygame.display.update()# update the window every time the loop runs