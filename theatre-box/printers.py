from colorama import Fore, Back, Style, init

# Initialize Colorama
init(autoreset=True)
def pretty_print(content):
    print(Back.MAGENTA + content)
    print("")
    print("")
    print("")

def print_with_background(text, foreground=Fore.CYAN, background=Back.BLACK, is_selected=False, total_width=60):
    # Choose a different background for the selected option
    selected_background = Back.MAGENTA if is_selected else background
    # Calculate padding
    padding = total_width - len(text)
    # Create padded text
    padded_text = text + ' ' * padding
    # Print with colors and padding
    print(f'{selected_background}{foreground}{padded_text}{Style.RESET_ALL}')

def print_dialogue(content, voice="nova"):
    color = Fore.GREEN
    if (voice == "fable") | (voice == "onyx" )| (voice == "echo"):
        color = Fore.RED
    else:
        color = Fore.CYAN

    merged_text = "\n".join(content["content"])
    print(content["name"] + ": " + color + Back.BLACK  + merged_text)

    print(Style.RESET_ALL)

def print_section(title, options, selected_option, background_color):
    print(Style.BRIGHT + Fore.BLACK + title)

    max_length = max(len(option) for option in options) + len("Option X: ") + 4  # Calculate max length for padding
    if title == "SETTINGS":
        for idx, option in enumerate(options, 1):
            # Construct the option text with "Option X:" format
            option_text = f"Option {idx}: {option}"
            # Highlight the selected option
            is_selected = (option == selected_option)
            print_with_background(option_text, Fore.BLACK, background_color, is_selected, total_width=max_length)
    else:
         for idx, option in enumerate(options, 1):
            # Construct the option text with "Option X:" format
            letters = { 1: "A", 2: "B", 3: "C" }
            option_text = f"Option {letters.get(idx)}: {option}"
            # Highlight the selected option
            is_selected = (option == selected_option)
            print_with_background(option_text, Fore.BLACK, background_color, is_selected, total_width=max_length)
    print(Style.RESET_ALL)  # Reset style after section

def print_current_prompt(setting, style, drama, comedy, total_width=60, print_dials=False):
    # Header for the current prompt section
    print_with_background("Your scene will be: ", Fore.BLACK, Back.CYAN, total_width=total_width)
    # Details of the current prompt with padding
    print_with_background(f"in the STYLE of: {style}", Fore.BLUE, Back.BLACK, total_width=total_width)
    print_with_background(f"in the SETTING of: {setting}", Fore.GREEN, Back.BLACK, total_width=total_width)
    if print_dials:
        print_with_background(f"Drama: {drama}/100", Fore.MAGENTA, Back.BLACK, total_width=total_width)
        print_with_background(f"Comedy: {comedy}/100", Fore.YELLOW, Back.BLACK, total_width=total_width)
    # Instruction to confirm the selection
    print(f"{Back.RED}Press the RED BUTTON to CONFIRM{Style.RESET_ALL}")

def main():
    print_dialogue
#     scenes = {
#         "Carnival": "backgrounds/Carnival_1.png",
#         "Dream": "backgrounds/Carol Style .png",
#         "City street": "backgrounds/City Street 1.png",
#         "Diner": "backgrounds/Diner .png",
#         "Enchanted mushroom forest": "backgrounds/Ench.png",
#         "Enchanted forest": "backgrounds/Enchanted.png",
#         "Fairytale castle": "backgrounds/Fairytale Castle.png",
#         "Hairdressers": "backgrounds/Hairdressers.png",
#         "Pirate Ship": "backgrounds/pirateship1.png",
#         "Mars after a spaceship crash": "backgrounds/Mars New 2.png",
#         "Mars": "backgrounds/Mars.png",
#         "Dreamworld": "backgrounds/Psychedelic Dreamscape.png",
#         "Kopli tram": "backgrounds/Kopli tram 1.png",
#         "Restaurant": "backgrounds/Restaurant 3.png",
#         "Steampunk Airship": "backgrounds/Steampunk Airship 1.png",
#         "Airship bridge": "backgrounds/Steampunk Airship 2.png",
#         "Grand Budapest Hotel Lobby": "backgrounds/Wes Anderson 2.png"
#     }
#     all_styles = ["Romeo and Juliet", "Rap battle", "West Side Story"]
#     all_settings = list(scenes.keys())
#     selected_style = "Rap battle"
#     selected_setting = "90s Kopli tram"
#     drama = 60
#     comedy = 40
#
#     # Find the maximum length of all options to set uniform width
#     total_width = max(max(len(s) for s in all_styles + all_settings) + 20, 60)
#
#     # Print style and setting options with one selected
#     print_section("STYLES", all_styles, selected_style, Back.RED)
#     print_section("SETTINGS", all_settings, selected_setting, Back.GREEN)
#
#     # Print current prompt details
#     print_current_prompt(selected_style, selected_setting, drama, comedy, total_width=total_width)

if __name__ == "__main__":
    main()
