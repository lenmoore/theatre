import pygame

def main():
    print("hey")
    pygame.mixer.init() # Initialize the mixer module
    background_music = pygame.mixer.Sound("music/theme.mp3") # file
    print(background_music)
    background_channel = pygame.mixer.Channel(0)  # Assign background music to channel 0
    background_channel.play(background_music, loops=-1)  # -1 means the music will loop indefinitely
#     background_music.set_volume(0)
    # Ensure the background music continues to play
#     if not background_channel.get_busy():
#         background_channel.play(background_music, loops=-1)




if __name__ == "__main__":
    main()
