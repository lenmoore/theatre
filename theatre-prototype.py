import cv2
import os

# Pretty printing function
def pretty_print(message):
    print(f"\n=== {message} ===\n")

# Function to capture an image
def capture_image(filename='photo.jpg'):
    cap = cv2.VideoCapture(0)  # 0 is typically the default webcam
    ret, frame = cap.read()
    if ret:
        # Ensure the 'pictures' directory exists
        if not os.path.exists('pictures'):
            os.makedirs('pictures')
        # Save the image
        cv2.imwrite(os.path.join('pictures', filename), frame)
    cap.release()
    return ret

# Main program
def main():
    pretty_print("Welcome to the improv theatre scene generator!")

    # Style selection
    styles = {
        'a': 'Romeo and Juliet',
        'b': 'Sopranos',
        'c': 'Star Trek'
    }
    for key, value in styles.items():
        print(f"{key}) {value}")
    style_choice = input("Please select a style you like: ")
    style = styles.get(style_choice, "Unknown")

    # Setting selection
    settings = {
        'a': 'Mars',
        'b': 'Hairdresser',
        'c': 'Classroom'
    }
    for key, value in settings.items():
        print(f"{key}) {value}")
    setting_choice = input("Please select a setting for the scene: ")
    setting = settings.get(setting_choice, "Unknown")

    # Funniness vs. Dramaticness
    scale = input("Please enter a value from 0 (funny) to 100 (dramatic): ")
    scale = min(max(int(scale), 0), 100)  # Ensure the value is between 0 and 100

    # Taking a photo
    if capture_image():
        pretty_print("Image Captured Successfully!")
    else:
        pretty_print("Failed to capture image.")

    # Combine inputs into a string
    prompt = f"Please generate a two-minute improv theatre scene with the characters on the image. Setting: {setting}; Style: {style}; Funnyness {100-scale}; Dramaticness {scale}."
    pretty_print(f"Resulted prompt would be: {prompt}")

if __name__ == "__main__":
    main()
