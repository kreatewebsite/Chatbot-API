import streamlit as st

import os
from main import get_answ,upload_documnt,get_embaddings,get_ans
from langchain import PromptTemplate, LLMChain
from llm_rag import ans_llm
# os.environ["TOKENIZERS_PARALLELISM"] = "false"
# template = """[INST] <<SYS>>
# You are a helpful, respectful and honest assistant. Answer the exact the question
# <</SYS>>

# Answer the question below from context below :
# {context}
# {question} [/INST]
# """
# config = {'max_new_tokens': 100, 'temperature': 0}
# llm = CTransformers(model='TheBloke/Llama-2-7B-Chat-GGML', config=config)
# re=[]
st.write("Qustion Matgpping App")
question=st.text_input("Ans Quesiton", key="question")
threshhold = st.slider('set a threshold', 0, 100, 70)
topk = st.slider('set top k answers', 0, 20, 5)
an=get_answ(question,"kk",topk,threshhold)
if(st.button("Find questions Ans answers")):
    if len(an)!=0:
     cnt=0
     for i in an:
        cnt+=1
    # st.write(f"Question {cnt}:", i)
        st.write(f"Answer {cnt}:", i)
    else:
      st.write("No answer in database")
if(st.button("get answer from chatgpt ans upload it to db")):
    ans_from_chat_gpt=upload_documnt(question,'kk')
    st.write("Answer :",ans_from_chat_gpt)
if(st.button("Answer From rag")):
    ans_from_chat_gpt=ans_llm(question)
    st.write("Answer :",ans_from_chat_gpt)
