from colorama import Fore, Back, Style
print(Style.RESET_ALL)

def print_dialogue(content, voice="nova"):
    color = Fore.MAGENTA
    color_back = Back.GREEN
    if voice == "nova":
        color = Fore.CYAN
    elif voice == "shimmer":
        color = Fore.MAGENTA
    elif voice == "fable":
        color = Fore.YELLOW
    elif voice == "echo":
        color = Fore.BLUE
    elif voice == "onyx":
        color = Fore.RED
    else:
        color = Fore.WHITE

    merged_text = "\n".join(content["content"])
    print(content["name"] + ": " + color + color_back + merged_text)

    print(Style.RESET_ALL)

def print_scene_name(content):
#     print(Fore.RED + content["name"] + ":")
#     print(Fore.GREEN + content["content"].join("..."))
    print(Style.RESET_ALL)

def prompt_print(all_styles, all_settings, setting, style, drama, comedy):
    print(Fore.WHITE + "The options for the STYLES are as follows: ")
    print(Back.RED + "    Option 1: " + Back.BLUE + all_styles[0])
    print(Back.RED + "    Option 2: " + Back.BLUE + all_styles[1])
    print(Back.RED + "    Option 3: " + Back.BLUE + all_styles[2])

    print(Style.RESET_ALL)

    print(Fore.WHITE + "The options for the SETTINGS are as follows: ")
    print(Back.WHITE + "    Option 1: " + Back.GREEN + all_settings[0])
    print(Back.WHITE + "    Option 2: " + Back.GREEN + all_settings[1])
    print(Back.WHITE + "    Option 3: " + Back.GREEN + all_settings[2])
    print(Style.RESET_ALL)

    print(Back.CYAN + Fore.BLACK + "The current prompt is: ")
    print(Back.BLACK + Fore.WHITE + "STYLE: " + Back.BLACK + Fore.BLUE + style)
    print(Back.RED + "SETTING: " + Back.BLACK + Fore.BLUE + setting)
    print("Drama" + Fore.BLUE + str(drama) + Fore.GREEN + "/100")
    print("Comedy" + Fore.YELLOW + str(comedy) + Fore.WHITE + "/100")
    print(Style.RESET_ALL)

#     message = (f"""The current prompt is:

#                     Setting: {setting}
#                        Style: {style}
#                       Drama: {drama}/100
#                    Comedy: {comedy}/100
#            When you are totally sure that you're ready with the prompt,'
#                   press START.
#
# """)
#     decoded = bytes(message, "utf-8").decode("unicode_escape")
#     print(decoded)


def prompt_print_no_start(setting, style, drama, comedy):
    print(Style.RESET_ALL)

    print(Back.CYAN + Fore.BLACK + "The final prompt is: ")
    print(Back.RED + "STYLE: " + Back.BLACK + Fore.BLUE + bytes(setting, "utf-8").decode("unicode_escape"))
    print(Back.BLACK + Fore.WHITE + "SETTING: " + Back.BLACK + Fore.BLUE + bytes(style, "utf-8").decode("unicode_escape"))
    print("Drama" + Fore.BLUE + bytes(str(drama), "utf-8").decode("unicode_escape") + Fore.GREEN + "/100")
    print("Comedy" + Fore.YELLOW + bytes(str(comedy), "utf-8").decode("unicode_escape") + Fore.WHITE + "/100")
    print(Style.RESET_ALL)


def pretty_print(message):
    print(Style.RESET_ALL)

# >>> decoded_string = bytes(myString, "utf-8").decode("unicode_escape") # python3
    print(Fore.WHITE, "====>")
    decoded = bytes(message, "utf-8").decode("unicode_escape")
    print(Fore.CYAN, decoded)
    print(Fore.WHITE, "")
    print(Fore.WHITE, "")
    print(Fore.WHITE, "")
    print(Fore.WHITE, "")
    print(Fore.WHITE, "")
    print(Style.RESET_ALL)


def main():
    something = { "name": "Director", "content": "Hello! I am the Director. Let's get started!"}
    something_else = { "name": "Director", "content": "Hello! I am the Director. Let's get started!"}
    print_dialogue(something, "nova")
    print_dialogue(something_else, "onyx")
    print_dialogue(something, "echo")
    print_dialogue(something_else, "fable")



if __name__ == "__main__":
    main()