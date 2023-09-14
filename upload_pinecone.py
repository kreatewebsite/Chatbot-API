import os
import PyPDF2
from bs4 import BeautifulSoup
import docx
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import pandas as pd
import uuid
import pinecone
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
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

def load_folder(file_path,name):
    
    # data = []
    extracted_text = ""

    file_extension = os.path.splitext(name)[1].lower()
    if file_extension == '.pdf':
        try:
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    extracted_text += page.extract_text()

        except PyPDF2.utils.PdfReadError:
            try:
                images=convert_from_path(file_path)
                for image in images:
                    text = pytesseract.image_to_string(image)
                    extracted_text += text
            except Exception as e:
                return f"An error occurred during OCR: {str(e)}"

    elif file_extension == '.html':
        with open(file_path, 'r', encoding='utf-8') as html_file:
            html_text = html_file.read()
            soup = BeautifulSoup(html_text, 'html.parser')
            extracted_text += soup.get_text()

    elif file_extension == '.docx':
        doc = docx.Document(file_path)
        extracted_text = ""
        for paragraph in doc.paragraphs:
            extracted_text += paragraph.text

    print("text_extracted")
    return  extracted_text

def create_text_chunks(text, chunk_size):
    # Process the text using spaC
    words = word_tokenize(text)
    chunks = []
    current_chunk = []
    current_chunk_word_count = 0
    
    for word in words:
        current_chunk.append(word)
        current_chunk_word_count += 1
        
        if current_chunk_word_count >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_chunk_word_count = 0
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    print("chunking done")
    
    return chunks
def get_embaddings(sentences):
    embeddings = model.encode(sentences)
    return embeddings

def up_pine(path,file_name):
   pdf_text=load_folder(path,file_name)
   tt=create_text_chunks(pdf_text, chunk_size=100)
   data = {"content":tt}
   df = pd.DataFrame(data)
   df['embeddings']=df['content'].apply(get_embaddings)
   index = pinecone.Index(index_name="kk")
   for i in range(len(df)):
    try:
       vec_response=index.upsert(vectors=[{'id': str(uuid.uuid4()), "values":df['embeddings'][i].tolist(), "metadata": {'answer':df['content'][i]}}])
    except:
       continue
   print("up_pine")

