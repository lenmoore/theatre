import base64
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
# oh whatever this is archived
OPENAI_KEY = os.getenv("OPENAI_KEY")

client = OpenAI()

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "../pictures/photo.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {OPENAI_KEY}"
}

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
        "text": "Please generate a two-minute improv theatre scene with the characters on the stage in the attached picture. Setting: Mars; Style: Romeo and Juliet; Funnyness 0; Dramaticness 100."
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
  max_tokens=300,
)
print(response.choices[0].message.content)
