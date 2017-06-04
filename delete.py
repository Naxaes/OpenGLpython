import pygame
pygame.init()

screen = pygame.display.set_mode((480, 480))
clock  = pygame.time.Clock()

time = 0
while True:
    time += clock.tick(2) / 1000


    if time < 2:
        pygame.event.pump()
    else:
        print(len(pygame.event.get()))


    pygame.display.update()