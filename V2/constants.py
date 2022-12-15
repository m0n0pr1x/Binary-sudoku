import pygame
X_IMAGE = pygame.transform.scale(pygame.image.load("images/x.png"), (80, 80))
O_IMAGE = pygame.transform.scale(pygame.image.load("images/o.png"), (80, 80))
X_init_IMAGE = pygame.transform.scale(pygame.image.load("images/1_init.png"), (80, 80))
O_init_IMAGE = pygame.transform.scale(pygame.image.load("images/0_init.png"), (80, 80))
VIDE_IMAGE = pygame.transform.scale(pygame.image.load("images/vide.png"), (80, 80))
ERREUR = pygame.transform.scale(pygame.image.load("images/ERREUR.png"), (150, 150))
VICTORY = pygame.transform.scale(pygame.image.load("images/victory.png"), (600,246))
WIDTH = 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CRASH_SOUND = "sounds/cute-uwu.mp3"
VICTORY_SOUND = "sounds/victory.mp3"
