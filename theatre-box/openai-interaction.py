from image_encoder import encode_image
import requests
from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")

client = OpenAI(api_key=OPENAI_KEY)

  # Correct way to set the API key


def create_openai_request(image_path):
    # Encode the image
    base64_image = encode_image(image_path)


    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "I'm generating an improv theatre scene with the characters in the image. Please tell me who they are in the following format. LEFT: [character name]=[character clothes, profession, role: antagonist/protagonist], RIGHT: [character name]=[character clothes, profession, role: antagonist/protagonist]. PROPS: [props or other creatures in the scene]."
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
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json())
    return response.json()


def create_openai_scene(input):
    
    prompt =f"Please generate a two-minute improv theatre scene with these characters: {input}. Write in a dialogue format with the character names and roles given to you in the input. Setting: Mars; Style: Romeo and Juliet; Funnyness 0; Dramaticness 100. It should last two minutes or be 320 words for the"
    print(prompt)
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
        {
        "role": "system", 
        "content": "You are a wonderfully funny TheatreBot, trained in the best methods of improv theatre. Your task is to generate the funniest text imaginable, and output it using JSON."
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
    print(response.choices[0].message.content)
    # print(response)



# Example usage
if __name__ == "__main__":
    image_path = "../pictures/Photo March 2 2024.jpg"
    result = create_openai_request(image_path)
    scene = create_openai_scene(result)
    print(scene)
