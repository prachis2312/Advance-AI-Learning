import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client=OpenAI(
    base_url=os.getenv("Base_URL"),
    api_key=os.getenv("API_KEY")
)

full_response=""

stream=client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[
        {
            "role":"user",
            "content":"Explain what is an API in 100 words"
        }
    ],
    stream=True

)


for chunk in stream:
    if not chunk.choices:
        continue
    piece=chunk.choices[0].delta.content
    if piece:
        print(piece,end="",flush=True)
        full_response+=piece

