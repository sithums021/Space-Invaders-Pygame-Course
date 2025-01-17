import pygame
from pygame import mixer
import random
import math

pygame.init()

#Setting the size of the screen
screen = pygame.display.set_mode((800, 600))

#Background and background music
background = pygame.image.load('background.png')
mixer.music.load('space-120280.mp3')
mixer.music.play(-1)

#Changing the title and icon of the pop window
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('001-galaxy.png')
pygame.display.set_icon(icon)

# Setting the image and location of player
player_img = pygame.image.load('001-spaceship.png')
player_x = 350
player_y = 480
x_change_player = 0

# Creating Enemies
# Multiple enemies will be used, so lists are used
enemy_img = []
enemy_x = []
enemy_y = []
x_change_enemy = []
y_change_enemy = []
no_enemies = 6

for i in range(no_enemies):
    enemy_img.append(pygame.image.load('001-alien-pixelated-shape-of-a-digital-game.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(0, 200))
    x_change_enemy.append(2)
    y_change_enemy.append(30)

# Setting up the bullet(s)
bullet = pygame.image.load('001-bullet.png')
bullet_x = 0
bullet_y = 480
y_change_bullet = 3
bullet_state = 'Ready'

# For keeping track and displaying the score
score = 0
font = pygame.font.Font('freesansbold.ttf', 52)
score_x = 10
score_y = 10

#font used for the "game over" sign
gameoverfont = pygame.font.Font('freesansbold.ttf', 100)

# imageLoad: for loading up images using screen.blit on the screen
# takes in the file and the co-ordinates to display them in
def imageLoad(image, x, y):
    screen.blit(image, (x, y))

# textLoad: for rendering and loading texts on the screen, takes the same inputs as imageLoad
def textLoad (text, x, y):
    score = font.render("Score : "+str(text), True, (255, 255, 255))
    screen.blit(score, (x,y))

# fireBullet: a function that runs all the necessary lines when the command to shoot a bullet is hit
def fireBullet(x, y):
    global bullet_state
    bullet_state = 'Fire'
    screen.blit (bullet, (x+16,y+10))

# resetBullet: to reset everything re: the bullet when the bullet reaches its end
def resetBullet():
    global bullet_state
    global bullet_y
    bullet_state = 'Ready'
    bullet_y = 480

# collisionDetector: to detect collisions
def collisionDetector (x1, y1, x2, y2):
    collision = math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))
    return collision<30

#gameOver: To display the game over sign
def gameOver (font):
    text = font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(text, (85, 250))

running = True
while running:
    imageLoad (background, 0, 0)
    for event in pygame.event.get():
        # exit the game if the close button is pressed
        if event.type == pygame.QUIT: 
            running = False

        # different scenarios if different keys are pressed
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change_player = -4

                if event.key == pygame.K_RIGHT:
                    x_change_player = 4

                if event.key == pygame.K_SPACE:
                    if bullet_state == 'Ready':
                        # creating a bullet sound for initiating the bullet leaving the spaceship
                        bullet_sound = mixer.Sound('Laser sound.mp3')
                        bullet_sound.play()
                        bullet_x = player_x #get current x co-ordinate of the spaceship
                        fireBullet(bullet_x, bullet_y)
        
        # different scenarios if different keys are released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change_player = 0
            
    player_x += x_change_player
    # making sure the player does not go out of bounds
    if player_x <= 0:
        player_x = 0
    elif player_x >=736: #subtract 64 pixels (size of the image) from the total amount of pixels
        player_x = 736

    # making sure the bullet persists until it reaches the boundary
    if bullet_state == 'Fire':
        fireBullet(bullet_x, bullet_y)
        bullet_y -= y_change_bullet
    if bullet_y<=0: resetBullet()

    # displaying and moving the enemies
    for i in range (no_enemies):
        enemy_x[i] += x_change_enemy[i]
        if enemy_x[i] <= 0:
            x_change_enemy[i] = 2
            enemy_y[i] += y_change_enemy[i]
        elif enemy_x[i] >=736: #subtract 64 pixels (size of the image) from the total amount of pixels
            x_change_enemy[i] = -2
            enemy_y[i] += y_change_enemy[i]
        
        # to check whether the enemy is close enough to the spaceship to call it game
        if enemy_y[i]>450:
            for j in range (no_enemies):
                mixer. music. stop()
                enemy_y[j] = 1000
                screen.fill((83, 183, 173))
                player_y = 1000
                gameOver(gameoverfont)


        # collision detection
        collision = collisionDetector(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            collision_sound = mixer.Sound('explosion sound.mp3')
            collision_sound.play()
            resetBullet()
            #respawning the enemy & updating the score
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(0, 200)
            score += 1
        
        imageLoad(enemy_img[i], enemy_x[i], enemy_y[i])

    imageLoad(player_img, player_x, player_y)
    textLoad(score, score_x, score_y)
    pygame.display.update()