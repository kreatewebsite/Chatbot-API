from sentence_transformers import SentenceTransformer
import pinecone
import uuid
import os
import openai
from config import OPENAI,PINECONE
openai.api_key = OPENAI
pinecone.init(api_key = PINECONE,
              environment="us-east4-gcp")
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2') 
def get_ans(qustion):
    model_engine = "text-davinci-003"
    prompt = qustion

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    return response
def get_embaddings(sentences):
    embeddings = model.encode(sentences)
    return embeddings
def upload_documnt(question,index_name):
  try:
      pinecone.create_index(index_name, dimension=768)
  except:
      print("index already created")
  index = pinecone.Index(index_name)
  
  emb=get_embaddings(question)
  answer=get_ans(question)
  try:
    upsert_response = index.upsert(
    vectors=[
        {'id': str(uuid.uuid4()), "values":emb.tolist(), "metadata": {'answer': answer,'question':question}},
    ]
    )
  except:
    return "Error Occured"
  
if __name__ == "__main__":
    query="what is ML?"
    aa=get_ans(query)
    print(aa)  
