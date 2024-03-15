from colorama import Fore, Back, Style
print(Style.RESET_ALL)

def print_dialogue(content):
    print(Fore.RED + content["name"] + ":")
    print(Fore.GREEN + content["content"])
    print(Style.RESET_ALL)

def print_scene_name(content):
    print(Fore.RED + content["name"] + ":")
    print(Fore.GREEN + content["content"].join("..."))
    print(Style.RESET_ALL)

def prompt_print(setting, style, drama, comedy):
    message = (f"""           The current prompt is:
                       Please generate a two-minute improv theatre scene
                     with the characters on the stage.
                   Setting: {setting}
                       Style: {style}
                      Drama: {drama}/100
                   Comedy: {comedy}/100
           When you are totally sure that you're ready with the prompt,'
                  press START.

""")
    decoded = bytes(message, "utf-8").decode("unicode_escape")
    print(decoded)


def prompt_print_no_start(setting, style, drama, comedy):
    message = (f"""           The final prompt is:
                        Please generate a two-minute improv theatre scene
                        with the characters on the stage.
                        Setting: {setting}
                        Style: {style}
                        Drama: {drama}/100
                        Comedy: {comedy}/100
""")
    decoded = bytes(message, "utf-8").decode("unicode_escape")
    print(decoded)




def pretty_print(message):

# >>> decoded_string = bytes(myString, "utf-8").decode("unicode_escape") # python3
    print(Fore.WHITE, "====>")
    print(Fore.WHITE, "")
    print(Fore.WHITE, "")
    print(Fore.WHITE, "")
    decoded = bytes(message, "utf-8").decode("unicode_escape")
    print(Fore.CYAN, decoded)
    print(Fore.WHITE, "")
    print(Fore.WHITE, "")
    print(Fore.WHITE, "")
