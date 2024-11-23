import pygame

pygame.init()

size = (800,800)

screen = pygame.display.set_mode(size) 
pygame.display.set_caption("Space shooter")

clock = pygame.time.Clock()

done = False
font = pygame.font.Font(pygame.font.get_default_font(), 36)

while not done:
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    #control game logic

    #drawing
    screen.fill((250, 250, 250))
    text_surface = font.render("Hello world", True, (0, 0, 0))
    screen.blit(text_surface, dest=(0,0))

    pygame.display.flip()
    clock.tick(30)


# now print the text