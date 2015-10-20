# KOD POBRANY I ZMODYFIKOWANE

import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

def get_key(dane):
  while not dane.exit:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    elif event.type == pygame.QUIT:
		dane.exit = True

def display_box_disabled(screen,rect, message):
  fontobject = pygame.font.SysFont('Calibri',60)
  pygame.draw.rect(screen, (255,255,255),
                   (rect[0],rect[1],rect[2]-2,rect[3]-4), 0)
  pygame.draw.rect(screen, (0,0,0),rect, 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (0,0,0) ),
                (rect[0],rect[1]) )
  pygame.display.flip()
		
def display_box(screen,rect, message):
  fontobject = pygame.font.SysFont('Calibri',60)
  pygame.draw.rect(screen, (172, 225, 175),
                   (rect[0],rect[1],rect[2]-2,rect[3]-4), 0)
  pygame.draw.rect(screen, (0,0,0),rect, 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (0,0,0) ),
                (rect[0],rect[1]) )
  pygame.display.flip()

def ask(screen,rect, question,dane):
	"ask(screen, rect question) -> answer"
	pygame.font.init()
	current_string = []
	display_box(screen,rect ,question + string.join(current_string,""))
	while not dane.exit:
		for event in pygame.event.get() :
			if event.type == pygame.QUIT:
				dane.exit = True
		inkey = get_key(dane)
		if inkey != None:
			if inkey == K_BACKSPACE:
				current_string = current_string[0:-1]
			elif inkey == K_RETURN:
				break
			elif inkey <= 127:
				current_string.append(chr(inkey))
			display_box(screen,rect, question + string.join(current_string,""))
	return string.join(current_string,"")

  
