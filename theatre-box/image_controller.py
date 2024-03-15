import pygame
carnival = "backgrounds/Carnival_1.png"

def open_image():
    pygame.init()
    screen = pygame.display.set_mode((1200, 900))
    background = pygame.image.load(carnival)
    screen.blit(background, (0, 0))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()


if __name__ == "__main__":
    open_image()