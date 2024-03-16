from colorama import Fore, Back, Style, init

# Initialize Colorama
init(autoreset=True)

def print_with_background(text, foreground=Fore.CYAN, background=Back.BLACK, is_selected=False, total_width=60):
    # Choose a different background for the selected option
    selected_background = Back.MAGENTA if is_selected else Back.BLACK
    # Calculate padding
    padding = total_width - len(text)
    # Create padded text
    padded_text = text + ' ' * padding
    # Print with colors and padding
    print(f'{selected_background}{foreground}{padded_text}{Style.RESET_ALL}')

def print_section(title, options, selected_option, background_color):
    print(Style.BRIGHT + Fore.WHITE + title)
    max_length = max(len(option) for option in options) + len("Option X: ") + 4  # Calculate max length for padding
    for idx, option in enumerate(options, 1):
        # Construct the option text with "Option X:" format
        option_text = f"Option {idx}: {option}"
        # Highlight the selected option
        is_selected = (option == selected_option)
        print_with_background(option_text, Fore.WHITE, background_color, is_selected, total_width=max_length)
    print(Style.RESET_ALL)  # Reset style after section

def print_current_prompt(style, setting, drama, comedy, total_width=60):
    # Header for the current prompt section
    print_with_background("The current prompt is:", Fore.WHITE, Back.CYAN, total_width=total_width)
    # Details of the current prompt with padding
    print_with_background(f"STYLE: {style}", Fore.BLUE, Back.BLACK, total_width=total_width)
    print_with_background(f"SETTING: {setting}", Fore.GREEN, Back.BLACK, total_width=total_width)
    print_with_background(f"Drama: {drama}/100", Fore.MAGENTA, Back.BLACK, total_width=total_width)
    print_with_background(f"Comedy: {comedy}/100", Fore.YELLOW, Back.BLACK, total_width=total_width)
    # Instruction to confirm the selection
    print(f"{Back.RED}Press the RED BUTTON to CONFIRM{Style.RESET_ALL}")

def main():
    all_styles = ["Romeo and Juliet", "Rap battle", "West Side Story"]
    all_settings = ["Mars", "Haunted mansion", "90s Kopli tram"]

    selected_style = "Rap battle"
    selected_setting = "90s Kopli tram"
    drama = 60
    comedy = 40

    # Find the maximum length of all options to set uniform width
    total_width = max(max(len(s) for s in all_styles + all_settings) + 20, 60)

    # Print style and setting options with one selected
    print_section("STYLES", all_styles, selected_style, Back.RED)
    print_section("SETTINGS", all_settings, selected_setting, Back.GREEN)

    # Print current prompt details
    print_current_prompt(selected_style, selected_setting, drama, comedy, total_width=total_width)

if __name__ == "__main__":
    main()
