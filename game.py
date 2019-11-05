
from __future__ import division
import sys
import math
import random
import pygame
import time


# initialize some sound related stuff before anything else
pygame.mixer.init() 
pygame.mixer.pre_init(44100, -16, 2, 2048)

# initialize the pygame module
pygame.init()

def distance(a, b):
	return math.sqrt(sum([(a[i]-b[i])**2 for i in (0, 1)]))


class Moneybag(object):
	(START, TRAVELLING, SPENT, CAUGHT) = (0, 1, 2, 3) 
	duration = 30
	moneybag = pygame.image.load('moneybag.png')
	moneybag = pygame.transform.smoothscale(moneybag,(50,50))
	caught_sound = pygame.mixer.Sound('cash_register.wav')
	
	def __init__(self, start, target):
		self.position = list(start)
		self.target = target[:]
		self.speed= 5
		self.state = self.TRAVELLING
		self.font = pygame.font.Font('ABG.ttf', 100)
		self.rect = self.moneybag.get_rect()


	def draw_on(self, screen):		
		if self.state == self.TRAVELLING:
			self.rect = self.moneybag.get_rect()
			self.rect = self.rect.move(self.position[0]-self.rect.width/2,
								  self.position[1]-self.rect.height)
			screen.blit(self.moneybag, self.rect)
			
		elif self.state == self.CAUGHT:
			pass

			
		else:
			pass
			
		
		
	def caught(self):
		self.state = self.CAUGHT
		self.caught_sound.play()
		self.counter = 0	

	def advance(self):
		if self.state == self.TRAVELLING:
			v = [None, None]
			v[0] = self.target[0] - self.position[0]
			v[1] = self.target[1] - self.position[1]
			
			norm = math.sqrt(v[0]**2 + v[1]**2)
			if norm == 0:
				pass
			if norm <= self.speed:
				self.state = self.SPENT
			else:
				v[0] = self.speed * v[0] / norm
				v[1] = self.speed * v[1] / norm
			
				self.position[0] += v[0]
				self.position[1] += v[1]	
		
		
		

		else: #state is spent
			pass
					
class Cop(Moneybag):
	(START,TRAVELLING,SPENT,CAUGHT,GAMEOVER) = (0,1,2,3,5)
	moneybag = pygame.image.load('cop.png')
	moneybag = pygame.transform.smoothscale(moneybag,(70,70))
	caught_sound = pygame.mixer.Sound('police_siren.wav')

	def __init__(self, start, target):
		super(Cop, self).__init__(start, target)
		self.speed = 12

class Thief(object):
	def __init__(self):
		self.delta_x = 40
		self.image = pygame.image.load('thief.png')
		self.image = pygame.transform.smoothscale(self.image,(100,100))
		self.pos = [350, 500]
		self.delta_x = 40

	def draw_on(self,screen):
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(self.pos[0],
								   self.pos[1])
		screen.blit(self.image, self.rect)
	
class MyGame(object):
	
	(PLAYING,MENU,GAMEOVER) = (0 ,1, 2)
	def __init__(self):
		"""Initialize a new game"""
		# list of falling things
		self.falling_stuff = list()
		self.state = self.MENU

		self.thief = Thief()
		
		self.falling_cops = list()
		self.falling_moneybags = list()
		self.counter = 0
		self.score = 1
		
		#sound
		self.soundtrack = pygame.mixer.Sound('song.wav')
		self.soundtrack.set_volume(.5)
		self.soundtrack.play(-1)
		
		#text/font
		self.font = pygame.font.Font('ABG.TTF', 20)
		
		
		# set up a 800 x 600 window
		self.width = 800
		self.height = 600
		self.screen = pygame.display.set_mode((self.width, self.height))
		


		# Setup a timer to refresh the display FPS times per second
		self.FPS = 30
		self.REFRESH = pygame.USEREVENT+1
		pygame.time.set_timer(self.REFRESH, 1000//self.FPS)


		# Now just start waiting for events
		self.event_loop()

	def event_loop(self):
		"""Loop forever processing events"""
		while 1 < 2:
			event = pygame.event.wait() 

			# Player is asking to quit.
			if event.type == pygame.QUIT \
					or (event.type == pygame.KEYDOWN and 
						event.key == pygame.K_ESCAPE):
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:					
					self.thief.pos[0] += self.thief.delta_x
					if self.thief.pos[0] >= 800:
						self.thief.pos[0] = -100				
					
				if event.key == pygame.K_LEFT:
					self.thief.pos[0] -= self.thief.delta_x					
					if self.thief.pos[0] <= -100:
						self.thief.pos[0] = 800
				
				if event.key == pygame.K_SPACE:
					self.state = self.PLAYING
					
					
						
			elif event.type == self.REFRESH:
				if self.state == self.PLAYING:
					#money bags
					for i in self.falling_moneybags:			
						if i.rect.colliderect(self.thief.rect):
							i.caught()
							self.score += 100
							i.state = i.SPENT
					#cops
					for i2 in self.falling_cops:
						self.counter += 1
						if i2.rect.colliderect(self.thief.rect):
							i2.caught()
							self.score -= 700
							i2.state = i2.SPENT
							time.sleep(1)
							
					if random.randrange(60) == 0:
						x_pos = random.randint(0, self.width)
						self.a = Moneybag((x_pos, 0),
									 (x_pos, self.height))
						self.falling_moneybags.append(self.a)

					 # increases frequecy	
					if random.randrange(max(1, 100 - self.score//100))==0:
						x_pos = random.randint(0, self.width)
						self.b = Cop((x_pos, 0),
								(x_pos, self.height))
						self.falling_cops.append(self.b)
						
					for s in self.falling_moneybags:
						s.advance()
					
					for s2 in self.falling_cops:
						s2.advance()
					
					self.falling_moneybags = [m for m in self.falling_moneybags if m.state != m.SPENT]
					self.falling_cops = [m2 for m2 in self.falling_cops if m2.state != m2.SPENT]
					
				if self.score <= 0:
					self.state = self.GAMEOVER
				
				else:
					pass
					
					
								
				self.draw()
				
			# This is some event type we don't handle
			else:
				pass


	def draw(self):
		"""Draw the current status of the game"""

		# Clear the screen (fill with white).		 
		self.screen.fill((0, 0, 0))
		
		if self.state == self.MENU:
			text = self.font.render('CASH CATCHER', True, (255,0,0))
			rect = text.get_rect()
			rect = rect.move((self.width - rect.width)//2,
							 (self.height - rect.height)//2)
			self.screen.blit(text, rect)
			
			text = self.font.render('Press SPACE to play', True, (255,0,0))
			rect = text.get_rect()
			rect = rect.move((self.width - rect.width)//2,
							 (self.height - rect.height)//2 + 100)
			self.screen.blit(text, rect)
			
		if self.state == self.PLAYING:
			for a in self.falling_cops:
				a.draw_on(self.screen)
			for a in self.falling_moneybags:
				a.draw_on(self.screen)
	
			self.thief.draw_on(self.screen)
			
			text = self.font.render('Score : %d$' % self.score, True, (255,0,0))
			rect = text.get_rect()
			rect = rect.move(0 ,0)
			self.screen.blit(text,rect)
			
		if self.state == self.GAMEOVER:
			text = self.font.render('GAMEOVER!!!', True, (255,0,0))
			rect = text.get_rect()
			rect = rect.move((self.width - rect.width)//2,
							 (self.height - rect.height)//2)
			
			self.screen.blit(text, rect)

			
		
		
		

		# Draw all the missiles
		


		# Flip buffers so that everything we have drawn gets displayed.
		pygame.display.flip()


# hunt club and bank. southkeys1111111111

MyGame()