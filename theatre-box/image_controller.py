import pygame

def open_image(scene_name):
    pygame.init()
    screen = pygame.display.set_mode((1200, 900))

    image_paths = {
        "90s Kopli tram": "backgrounds/tram.jpeg",
        "Carnival": "backgrounds/Carnival_1.png",
        "Pirate Ship": "backgrounds/pirateship1.png",
        "Mars": "backgrounds/mars.webp",
        "Haunted": "backgrounds/haunted.png"
    }

    image = image_paths.get(scene_name, "backgrounds/Carnival_1.png")  # Default to Carnival if not found
    background = pygame.image.load(image)
    screen.blit(background, (0, 0))
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

if __name__ == "__main__":
    open_image("90s Kopli tram")
