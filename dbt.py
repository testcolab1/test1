sec_key ="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"


from langchain_huggingface import HuggingFaceEndpoint

import os
os.environ["HF_TOKEN"]=sec_key
os.environ["HUGGINGFACEHUB_API_TOKEN"]=sec_key
from langchain.prompts import PromptTemplate
from langchain import HuggingFaceHub
llm_huggingface=HuggingFaceHub(repo_id="google/flan-t5-large",model_kwargs={"temperature":0,"max_length":64})
from langchain.chains import LLMChain
repo_id= "mistralai/Mistral-7B-Instruct-v0.3"
llm=HuggingFaceEndpoint(repo_id=repo_id,max_length=128,temperature=0.7,token=sec_key)
prompt_template=PromptTemplate(input_variables=['country'],
template="Tell me the capital of this {country}")
chain=LLMChain(llm=llm,prompt=prompt_template)


from langchain.schema import HumanMessage,SystemMessage,AIMessage

chatllm=HuggingFaceHub(repo_id="google/flan-t5-large",model_kwargs={"temperature":0,"max_length":64})

from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser

class Commaseperatedoutput(BaseOutputParser):
    def parse(self,text:str):
        return text.strip().split(",")


template="Your are a helpful assistant. When the use given any input , you should generate 5 words synonyms in a comma seperated list"
human_template="{text}"
chatprompt=ChatPromptTemplate.from_messages([
    ("system",template),
    ("human",human_template)


])
chain=chatprompt|chatllm|Commaseperatedoutput()
import streamlit as st


st.set_page_config(page_title="dbt code generator")
st.header("lets chat")



if 'flowmwssage' not in st.session_state:
    st.session_state['flowmessage']=[
        SystemMessage(content="you are a dbt code generator the user can request a code block for bdt, but if the user ask any thing other than dbt code prompt to user taht u can only be used to generate dbt code only.")
    ]



def get_response(question):
    st.session_state['flowmessage'].append(HumanMessage(content=question))
    ans=llm.invoke(st.session_state['flowmessage'])
    st.session_state['flowmessage'].append(AIMessage(content=ans))
    return ans


input=st.text_input("Input:",key="input")
response=get_response(input)
submit=st.button("Submit")

if submit:
    st.subheader("The reponse is: ")
    st.write(response)