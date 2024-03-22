from image_encoder import encode_image
import requests
from openai import OpenAI
from pathlib import Path
import image_encoder
import json
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")

client = OpenAI(api_key=OPENAI_KEY)


def create_openai_request(base64_image, prompt):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_KEY}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I'm generating an improv theatre scene with the characters in the image. Even if the image is hard to see, please try your best. Please tell me who they are in the following format. LEFT: [character name]=[character clothes, profession, role: antagonist/protagonist, whisper: your recommendation for Whisper API voice], RIGHT: [character name]=[character clothes, profession, role: antagonist/protagonist, whisper: your recommendation for Whisper API voice]. PROPS: [props or other creatures in the scene]. Also, recommend suitable Whisper API voices for each character and a storyteller voice if necessary. the prompt that will be used for the text will be this:" + prompt + ".. so please make the characters match the scene."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4096
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json())
    return response.json()

def create_openai_scene(image_desc, prompt):
    print(prompt)
    response = client.chat.completions.create(
    response_format={ "type": "json_object" },
    model="gpt-4-turbo-preview",
    max_tokens=4096,
    messages=[
        {
        "role": "system", 
        "content": "You are a TheatreBot, trained in the best methods of improv and classical theatre. Your task is to generate the funniest text for a short scene imaginable, and output it using JSON. The voice options for the characters are as follows. alloy=deeper female. echo=average male. fable=male British. onyx=dark male, a little southern. nova=female, asserting. shimmer=female, soft, but feels hysteric. There can only be one storyteller and two characters. If the comedy is under 60, the scene will be in the style of Werner Herzog, the storyteller's voice' will be onyx."
        },
        {
        "role": "system",
        "content": "The structure needs to be like this: { scene_name: [scene name], dialogue: { [ { name: 'storyteller|name|name', content: [lines], voice: voice_selected_from_options } ] }  "
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            },

        ]
        }
    ]
    )

#     return response.choices[0].message.content
#     print(response)
#     something = response.json()
#     return something["choices"][0]["message"]["content"]
    return json.loads(response.choices[0].message.content)
    # print(response)

# files in the improv folder will be like
# 1_left_speech.mp3
# 2_right_speech.mp3
# 3_storyteller_speech.mp3
# etc
def get_whisper(order_number, voice, text, character="director"):
    speech_file_path = Path(__file__).parent / f"speech/director/{order_number}_{character}_speech.mp3"

    response = client.audio.speech.create(
      model="tts-1",
      voice=voice,
      input=text
    )
    if response:  # Assuming 'response' is a Response object
        response.stream_to_file(speech_file_path)
        return True
    return False
def get_improv_whisper(order_number, voice, text, character):
    speech_file_path = Path(__file__).parent / f"speech/improv/{order_number}_{character}_speech.mp3"

    response = client.audio.speech.create(
      model="tts-1",
      voice=voice,
      input=text
    )
    if response:  # Assuming 'response' is a Response object
        response.stream_to_file(speech_file_path)
        return True
    return False

# Example usage
if __name__ == "__main__":
    image_path = "../pictures/photo.jpg"
    base64_image = encode_image(image_path)
    prompt = "Please generate a 2-min improv theatre scene with the characters in the image. Setting: hairdresser's. Style: Romeo and Juliet. Comedy: 80. Drama: 20."
    result = create_openai_request(base64_image, prompt)
    scene = create_openai_scene(result, prompt)
    print(scene)


