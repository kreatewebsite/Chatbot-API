from config import *
from main import get_answ
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain import PromptTemplate
llm = OpenAI(openai_api_key=OPENAI)
template = """[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Answer the exact the question given in context
<</SYS>>

Answer the question below from context below :
{context}
{question} [/INST]
"""
def ans_llm(query):
   prompt = PromptTemplate(template=template, input_variables=["context", "question"])
   llm_chain = LLMChain(prompt=prompt, llm=llm)
   aa=get_answ(query,"kk",3,50)
   aa="".join(aa)
   response = llm_chain.run({"question":query,"context":aa})
   return response,aa





