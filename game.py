from config import *
from classes import Manager

clock = pygame.time.Clock()
manager = Manager(screen)
running = True

while running:
    manager.surface.fill(black)
    manager.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(100)