import pygame
import time

def play_music(file_path):
    # Initialize Pygame's mixer
    pygame.mixer.init()
    # Load the background music
    background_music = pygame.mixer.Sound(file_path)
    # Set the volume (0.0 to 1.0)
    background_music.set_volume(0.05)
    # Play the music, -1 means it will loop indefinitely
    background_music.play(-1)

    # Keep the program running while the music plays
    try:
        # Run until the music is stopped or an interrupt (Ctrl+C) is received
        while True:
            # You can replace this with any condition or just a simple time.sleep
            input("Press Enter to stop the music or Ctrl+C to exit.")
            break  # Exit the loop if the user presses Enter
    except KeyboardInterrupt:
        pass  # Catch the interrupt and pass to exit gracefully
    finally:
        # Stop the music and quit mixer
        background_music.stop()
        pygame.mixer.quit()

if __name__ == "__main__":
    # Path to your music file
    music_file = "music/theme.mp3"
    play_music(music_file)
