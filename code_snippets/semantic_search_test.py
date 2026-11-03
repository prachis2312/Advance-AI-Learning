import os
import numpy
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client=OpenAI(
    base_url=os.getenv("Base_URL"),
    api_key=os.getenv("API_KEY")
)

def get_embedding(text):
    response=client.embeddings.create(
        model=os.getenv("EMBED_MODEL"),
        input=text
    )

    return response.data[0].embedding

def cosine_similarity(A,B):
    dot_prod=numpy.dot(A,B)
    norm_a=numpy.linalg.norm(A)
    norm_b=numpy.linalg.norm(B)
    return dot_prod/(norm_a*norm_b)


text_1="Python is a good programming language"
text_2="Python is used to write AI related code snippets"
text_3="I Love eating apples every morning"

embed1=get_embedding(text_1)
embed2=get_embedding(text_2)
embed3=get_embedding(text_3)

similarity12=cosine_similarity(embed1,embed2)
similarity23=cosine_similarity(embed2,embed3)

print(f"{similarity12:.2f}")
print(f"{similarity23:.2f}")