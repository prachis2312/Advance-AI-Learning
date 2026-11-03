import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client=OpenAI(
    base_url=os.getenv("Base_URL"),
    api_key=os.getenv("API_KEY")
)

response=client.embeddings.create(
    model=os.getenv("EMBED_MODEL"),
    input=["I am a good boy","He studies for 6 hours a day"]
)

for i,emb in enumerate(response.data):
    print(f"embedding: {i} , length: {len(emb.embedding)}")
    print(emb.embedding[:5])
