import pygame
import random
import math
from pygame import mixer

# To initiate the game. Always added before any creating any game using pygame module.

pygame.init()

# create window for the game

screen = pygame.display.set_mode((800, 600))

# Game Title and icon
pygame.display.set_caption("Pineapple Invadors")
icon = pygame.image.load('C:\Projects\PP\PinappleInvadors/natural.png')  # directory of the image
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('C:\Projects\PP\PinappleInvadors/main2.png')
# Player coordinates on the screen (approximatly in the middle)
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 4

# Create for loop that will iterate as many as there are specified enemies
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('C:\Projects\PP\PinappleInvadors/peach2.png'))
    # randint is a method used to randomize integers between the two parameters you give it
    enemyX.append(random.randint(0, 733))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet

bulletImg = pygame.image.load('C:\Projects\PP\PinappleInvadors/heart.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
# Ready state - you cant see the bullet on the screen
# Fire state - the bullet is moving
bullet_state = "ready"
# Background
background = pygame.image.load('C:\Projects\PP\PinappleInvadors/bg3.png')

# Background music
mixer.music.load('C:\Projects\PP\PinappleInvadors/Fallin_-Love-MOTHER.wav')
mixer.music.play(-1)

# Score
score_value = 0
# pygame.font take two parameters the name of font and description as well as the size
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
# Function for player to appear on the screen

def player(x, y):
    # This method allows the player to be drawn on to the screen it takes two parameters the variable that contains the img and coordinates (x,y).
    screen.blit(playerImg, (playerX, playerY))


# x and y is for enemy coordinates and i is to identify which enemy it is
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# function for when the player presses space a bullet gets shot
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    # the values added to x and y is to make sure the bullet is in the middle of the player
    screen.blit(bulletImg, (x + 16, y + 10))


def showScore(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Game over function
def game_over_text():
    game_over_text = game_over_font.render("GAME OVER" , True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))


# Calculate the distance between the enemy and bullet
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# The loop that contains all game events
running = True
while running:
    # to change the color of the screen/background
    # screen.fill takes Red, Green, Blue values
    # The screen color should be the first line everything that goes on top of it will be under this line (like a stack)
    screen.fill((48, 25, 54))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if a keystroke is pressed check if its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.0
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.0
            if event.key == pygame.K_UP:
                playerY_change = -0.4
            if event.key == pygame.K_DOWN:
                playerY_change = 0.4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # sound effect for bullet
                    bullet_sound = mixer.Sound('C:\Projects\PP\PinappleInvadors/SVTFOE-Wand-Sound-Effect.wav')
                    bullet_sound.play()
                    # save state of player in the x-axis in bulletX
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # if a keystroke is being released check if its right or left
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                playerY_change = 0

    # call player and enemy and score function in the loop so it can appear on every frame of the screen
    player(playerX, playerY)
    showScore(textX, textY)
    # Updating the player movement variables with every keystroke
    playerX += playerX_change
    playerY += playerY_change

    # Create boundaries for the player in the x-axis

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Create boundaries for the player in the y-axis
    if playerY <= 360:
        playerY = 360
    elif playerY >= 536:
        playerY = 536

    # a for loop for all enemies movement and collision

    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 200:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # restart enemy position
            enemyX[i] = random.randint(0, 733)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # shoot multiple bullets by resting the bullet once it goes out of boundries

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    # Bullet movement

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # To keep updating the game screen (V.important)
    pygame.display.update()
