import pygame
carnival = "backgrounds/Carnival_1.png"
pirateship = "backgrounds/pirateship1.png"
mars = "backgrounds/mars.webp"
tram = "backgrounds/tram.jpeg"
haunted = "backgrounds/haunted.png"

def open_image(scene_name):
    if (scene_name == "90s Kopli tram"):
        image = tram
    pygame.init()
    screen = pygame.display.set_mode((1200, 900))
    background = pygame.image.load(image)
    screen.blit(background, (0, 0))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()


# def take_user_image():
#     # take an image with the computer webcam
#
# def take_stage_image():
#     # take an image with the external webcam
#

if __name__ == "__main__":
    global image
    image = carnival
    open_image("90s Kopli tram")