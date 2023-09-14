import os
import spacy
import PyPDF2
import pandas as pd
import uuid
import pinecone
from langchain.vectorstores import Pinecone
# import nltk
# nltk.download('punkt')
# from nltk.tokenize import word_tokenize

import uuid
from config import OPENAI,PINECONE

from sentence_transformers import SentenceTransformer
pinecone.init(api_key = PINECONE,
              environment="us-west1-gcp-free")
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2') 
index="kk"

def load_pdf(folder_path):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
      files = os.listdir(folder_path)
      for file in files:
          if file.endswith('.pdf'):
              pdf_file_path = os.path.join(folder_path, file)
              pdf_file = open(pdf_file_path, 'rb')
              pdf_reader = PyPDF2.PdfReader(pdf_file)
              pdf_text = ""
              # Iterate through each page and extract text
              for page_num in range(len(pdf_reader.pages)):
                  page = pdf_reader.pages[page_num]
                  pdf_text += page.extract_text()
              pdf_file.close()
              print(f"Text content of {file}:")
              print(pdf_text)
              return pdf_text

    else:
       print("Folder not found or is not a directory")
pdf_text=load_pdf("E:/test-main/travel.pdf")

nlp=spacy.load("en_core_web_sm")

def create_text_chunks(text, chunk_size):
    # Process the text using spaCy
    doc = nlp(text)

    chunks = []
    current_chunk = []
    current_chunk_word_count = 0

    for token in doc:
        current_chunk.append(token.text)
        current_chunk_word_count += 1

        if current_chunk_word_count >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_chunk_word_count = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
def get_embaddings(sentences):
    embeddings = model.encode(sentences)
    return embeddings
tt=create_text_chunks(pdf_text, chunk_size=100)
data = {"content":tt}
df = pd.DataFrame(data)
df['embeddings']=df['content'].apply(get_embaddings)
index = pinecone.Index(index_name=index)
for i in range(len(df)):
  try:
    vec_response=index.upsert(vectors=[{'id': str(uuid.uuid4()), "values":df['embeddings'][i].tolist(), "metadata": {'answer':df['content'][i]}}])
  except:
    continue


