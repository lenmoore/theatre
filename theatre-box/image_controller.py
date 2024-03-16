import os

import tkinter as tk
from tkinter import PhotoImage, Toplevel
import threading



image_paths = {
    "Carnival": "backgrounds/Carnival_1.png",
    "Dream": "backgrounds/Carol Style .png",
    "City street": "backgrounds/City Street 1.png",
    "Diner": "backgrounds/Diner .png",
    "Enchanted mushroom forest": "backgrounds/Ench.png",
    "Enchanted forest": "backgrounds/Enchanted.png",
    "Fairytale castle": "backgrounds/Fairytale Castle.png",
    "Hairdressers": "backgrounds/Hairdressers.png",
    "Pirate Ship": "backgrounds/pirateship1.png",
    "Mars after a spaceship crash": "backgrounds/Mars New 2.png",
    "Mars": "backgrounds/Mars.png",
    "Dreamworld": "backgrounds/Psychedelic Dreamscape.png",
    "Kopli tram": "backgrounds/Kopli tram 1.png",
    "Restaurant": "backgrounds/Restaurant 3.png",
    "Steampunk Airship": "backgrounds/Steampunk Airship 1.png",
    "Airship bridge": "backgrounds/Steampunk Airship 2.png",
    "Grand Budapest Hotel Lobby": "backgrounds/Wes Anderson 2.png"
}
def create_image_window(image_path, max_height=700):
    # Create a top-level window
    window = Toplevel()
    window.title("Image Display")

    # Load the image
    img = PhotoImage(file=image_path)

    # Resize image if it's taller than max_height
    img_width = img.width()
    img_height = img.height()
    if img_height > max_height:
        scale_factor = max_height / float(img_height)
        img_width = int(img_width * scale_factor)
        img_height = max_height
        img = img.subsample(int(1/scale_factor), int(1/scale_factor))

    # Create a label to display the image
    label = tk.Label(window, image=img)
    label.pack()

    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate position for the window to be at the bottom center
    x = (screen_width - img_width) // 2
    y = screen_height - img_height - 50  # 50 pixels from the bottom of the screen

    # Set the window size and position
    window.geometry(f'{img_width}x{img_height}+{x}+{y}')

    # This is necessary to keep a reference to the image object
    label.image = img

    window.mainloop()

def open_image_in_thread(image_path):
    # Run the create_image_window function in a separate thread
    thread = threading.Thread(target=create_image_window, args=(image_path,))
    thread.start()

# Example usage
if __name__ == "__main__":
    image_path = image_paths.get("Mars")  # Replace with your image path
    open_image_in_thread(image_path)

    # Your main program continues here
    print("Main program continues to run...")