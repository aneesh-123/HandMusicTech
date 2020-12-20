import pygame

pygame.init()
win = pygame.display.set_mode((100,100))

while True:
    for eve in pygame.event.get():pass
    keyInput = pygame.key.get_pressed()
    if keyInput [pygame.K_a]:
        print("key a pressed")
