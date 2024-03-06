
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




def pretty_print(message):
# >>> decoded_string = bytes(myString, "utf-8").decode("unicode_escape") # python3
    message = (f"""====> {message}
""")
    decoded = bytes(message, "utf-8").decode("unicode_escape")
    print(decoded)
