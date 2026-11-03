import os
import numpy
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client=OpenAI(
    base_url=os.getenv("Base_URL"),
    api_key=os.getenv("API_KEY")
)

EMBED_MODEL=os.getenv("EMBED_MODEL")
KB_FOLDER=os.getenv("KB_FOLDER")


def get_embedding(text):
    response=client.embeddings.create(
        model=EMBED_MODEL,
        input=text
    )
    return response.data[0].embedding


def cosine_similarity(A,B):
    dot_prod=numpy.dot(A,B)
    norm_a=numpy.linalg.norm(A)
    norm_b=numpy.linalg.norm(B)
    return dot_prod/(norm_a*norm_b)


def load_documents(folder=KB_FOLDER):
    documents=[]

    for filename in sorted(os.listdir(folder)):
        if not filename.endswith(".txt"):
            continue

        path=os.path.join(folder, filename)
        with open(path,"r",encoding="utf-8") as f:
            documents.append(
                {
                    "source":filename,
                    "text":f.read()
                }
            )

    return documents


def add_embeddings(documents):
    for doc in documents:
        emebdding=get_embedding(doc["text"])
        doc["vector"]=emebdding

    return documents

def search(query,documents,top_k=3):
    query_vector=get_embedding(query)

    results=[]

    for doc in documents:
        score=cosine_similarity(query_vector,doc["vector"])
        results.append(
            {
                "score":float(score),
                "source":doc["source"],
                "size":len(doc["text"])
            }
        )

    results.sort(key=lambda rec: rec["score"], reverse=True)
    return results[:top_k]

def test(user_query,documents,top_k=3):
    print(f"\nUser Query: {user_query}\n")
    results=search(user_query,documents,top_k)

    for r in results:
        print(f" {r['score']:.2f} - {r['source']} - {r['size']} characters")


documents=load_documents()
documents=add_embeddings(documents)

print(f"we have embedded {len(documents)} documents")

user_query="How many days will i get for maternity leave?"
test(user_query,documents,3)