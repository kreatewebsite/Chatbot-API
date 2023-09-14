# from langchain.document_loaders import UnstructuredPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
# import pinecone
from torch import index_copy
import uuid
import pinecone
from langchain.vectorstores import Pinecone
from sentence_transformers import SentenceTransformer
import openai
import os
from config import OPENAI,PINECONE

openai.api_key = OPENAI
pinecone.init(
    api_key=PINECONE,
    environment="us-west1-gcp-free"
)
index = "kk"
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2') 
def get_embaddings(sentences):
    embeddings = model.encode(sentences)
    return embeddings
def get_answ(query,index,top_k,threshold):
   query=get_embaddings(query).tolist()
   index = pinecone.Index(index_name=index)
   a=index.query(query, top_k=top_k, include_metadata=True)
   answers = []

   for result in a['matches']:
        score = result['score']
        metadata = result['metadata']

        # Compare the similarity score with the threshold
        if score >= (threshold / 100):
            answer = metadata.get('answer', None)
            if answer:
                answers.append(answer)

   return answers
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
def upload_documnt(question,index_name):
  try:
      pinecone.create_index(index_name, dimension=768)
  except:
      print("index already created")
  index = pinecone.Index(index_name)
  
  emb=get_embaddings(question)
  answer=get_ans(question)
  upsert_response = index.upsert(
    vectors=[
        {'id': str(uuid.uuid4()), "values":emb.tolist(), "metadata": {'answer': answer,'question':question}},
    ]
    )
  return answer
print(upload_documnt("what is machine learning","kk"))
