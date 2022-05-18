import pygame
import random
import numpy as np
from pygame import mixer

#initialize the pygame
pygame.init()  #must 1

#create the screen
screen = pygame.display.set_mode((800,600)) #(x,y) tuple value of screen size

#Title and Icon
pygame.display.set_caption("Space Invaders by Samy Oscar")
icon = pygame.image.load('gift-box.png') #loads the image
pygame.display.set_icon(icon)

#background
background=pygame.image.load('background.jpg')
background=pygame.transform.scale(background, (800,600))

#background music
mixer.music.load('bgm.mp3')
mixer.music.play(-1)

# Player
player_img=pygame.image.load('player.png')
playerX=370        #player img positions
playerY=500 
playerX_change=0          #variable for changing x value of spaceship

# Enemy
#arrays for appending the multiple enemy values
enemy_img= []
enemyX= []       #enemy img positions
enemyY= []
enemyX_change= []         #variable for changing x value of enemy
enemyY_change= []
enemy_num=8

for i in range(enemy_num):
	enemy_img.append(pygame.image.load('enemy.png'))
	enemyX.append(random.randint(0,735))        #enemy img positions
	enemyY.append(random.randint(0,300)) 
	enemyX_change.append(0.5)           #variable for changing x value of enemy
	enemyY_change.append(20)             #variable for changing y value of enemy

#bullet
bullet_img=pygame.image.load('bullet.png')
bulletX=0                             #bullet img positions
bulletY=480
bulletX_change=0           #variable for changing x value of bullet (which doesnt change)
bulletY_change=5             #variable for changing y value of enemy
bullet_state="ready"          #state of bullet; ready=we cant see bullet on screen; fire=bullet is currently moving


#score
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)

scoreX=10
scoreY=10

#GAME OVER text
game_over=pygame.font.Font('freesansbold.ttf',64)


def game_over_show():       #GAME OVER text
	game_over_text=game_over.render("GAME OVER", True, (255,255,255))
	screen.blit(game_over_text,(200,250))  #blit=draw

def show_score(x,y):    #function for displaying the game score
	score=font.render("Score: " + str(score_value), True, (255,255,255))
	screen.blit(score,(x,y))  #blit=draw

def player(x,y):    #function for drawing the player image on screen each time in the while loop
	screen.blit(player_img,(x,y))  #blit=draw

def enemy(x,y,i):    #function for drawing the enemy image on screen each time in the while loop
	screen.blit(enemy_img[i],(x,y))  #blit=draw

def fire_bullet(x,y):    #function for drawing the bullet image on screen each time in the while loop
	global bullet_state
	bullet_state="fire"
	screen.blit(bullet_img,(x+16,y+10))  #blit=draw

def isCollision(bulletX,bulletY,enemyX,enemyY):
	distance=np.sqrt((enemyX-bulletX)**2 + (enemyY-bulletY)**2)
	if distance <27:
		return True
	else: return False
    

#Game Loop
running = True
while running:
	screen.fill((182, 137, 192)) #tuple value of color of screen

	#background image
	screen.blit(background,(0,0))  #blit=draw , position of bg image starting point of drawing

	for event in pygame.event.get(): #fetch event properties
		if event.type==pygame.QUIT:   #type of event, Exit
			running=False

		if event.type==pygame.KEYDOWN:   #keydown=key press
			if event.key==pygame.K_LEFT:
				playerX_change= -0.7
			if event.key==pygame.K_RIGHT:
				playerX_change= 0.7
			if event.key==pygame.K_SPACE:
				if bullet_state == "ready":
					mixer.Sound('bullet.mp3').play()
					bulletX=playerX        #get current x coordinate of spaceship
					fire_bullet(bulletX,bulletY)

		if event.type==pygame.KEYUP:	#keyup=release key
			if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
				playerX_change= 0

	#player movement
	playerX+=playerX_change      #changing x value of player
	
	#Boundary of our game screen objects spaceship
	if playerX<=0:
		playerX=0
	elif playerX>=736:
		playerX=736


	#enemy movement
	for i in range(enemy_num):
		
		#GAME OVER text
		if enemyY[i] >440:
			for j in range(enemy_num):
				enemyY[j]=2000
			game_over_show() 
			break


		enemyX[i]+=enemyX_change[i]      #changing x value ofenemy

		#Boundary of our game screen objects enemy
		if enemyX[i]<=0:
			enemyX_change[i]=0.3
			enemyY[i]+=enemyY_change[i]              #for movement of the enemy when it touches the first boundary
		elif enemyX[i]>=736:             #for movement of the enemy when it touches the last boundary
			enemyX_change[i]=-0.3
			enemyY[i]+=enemyY_change[i]

		#collision
		collision=isCollision(bulletX,bulletY,enemyX[i],enemyY[i])

		if collision:
			mixer.Sound('collision.mp3').play()
			bulletY=480
			bullet_state="ready"
			score_value+=1                           #updates score
			enemyX[i]=random.randint(0,735)        #enemy respawns
			enemyY[i]=random.randint(0,300) 

		enemy(enemyX[i],enemyY[i],i)


	#bullet movement
	if bulletY<=0:
		bulletY=480
		bullet_state="ready"

	if bullet_state == "fire":
		fire_bullet(bulletX,bulletY)
		bulletY-=bulletY_change

	

	player(playerX,playerY)
	show_score(scoreX,scoreY)
	pygame.display.update()    #must 2, it update the values of screen continuously
