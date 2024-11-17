import pygame

pygame.init()

size = (800,800)

screen = pygame.display.set_mode(size) 
pygame.display.set_caption("Space shooter")

clock = pygame.time.Clock()

done = False

while not done:
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    #control game logic

    #drawing
    screen.fill((250, 250, 250))

    pygame.display.flip()
    clock.tick(30)