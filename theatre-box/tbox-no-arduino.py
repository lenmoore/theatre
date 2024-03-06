# this file assumes that I already have the prompt, and we press start, triggering the API call.

def main():
    print("Hello, I am the Director. Let's get started!")
    print("The current prompt is: ")
    print("Please generate a two-minute improv theatre scene with the characters on the stage.")
    print("Setting: Mars")
    print("Style: Romeo and Juliet")
    print("Drama: 0/100")
    print("Comedy: 0/100")
    print("When you are totally sure that you're ready with the prompt, press START.")

    # This is where the Arduino would be waiting for the start button to be pressed
    # and then it would send a signal to the Raspberry Pi to start the API call
    # but for the sake of this example, I will just print "API call made" when the start button is pressed
    start = input("Press START (write s and press enter) when ready: ")
    if start == "s":
        print("Going to make the API call now.")


if __name__ == "__main__":
    main()
