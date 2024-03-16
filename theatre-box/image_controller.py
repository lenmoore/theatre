import pygame
import os
from tkinter import Tk, Canvas, PhotoImage
os.environ['SDL_VIDEODRIVER'] = 'x11'
os.environ['SDL_VIDEO_CENTERED'] = '1'

image_paths = {
    "90s Kopli tram": "backgrounds/tram.jpeg",
    "Carnival": "backgrounds/Carnival_1.png",
    "Pirate Ship": "backgrounds/pirateship1.png",
    "Mars": "backgrounds/mars.webp",
    "Haunted": "backgrounds/haunted.png"
}

def open_image(image_path):
    root = Tk()
    canvas = Canvas(root, width=1200, height=900)
    canvas.pack()
    image = image_paths.get(image_path)
    img = PhotoImage(file=image)
    canvas.create_image(20, 20, anchor='nw', image=img)
    root.mainloop()
# def open_image(scene_name):
#     pygame.init()
#     screen = pygame.display.set_mode((1200, 900))
#
#
#
#     image = image_paths.get(scene_name, "backgrounds/Carnival_1.png")  # Default to Carnival if not found
#     background = pygame.image.load(image).convert()
# #     screen.blit(background, (background, 0))
# #     pygame.display.flip()
#
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#     pygame.quit()

if __name__ == "__main__":
    open_image("Carnival")
