from pprint import pprint

from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompt_values import PromptValue
from langchain_openai import ChatOpenAI
from dotenv import *
from langchain_core.runnables import RunnableLambda

#load_dotenv()

template = 'this is variable1={variable1}, and this is variable2={variable2}'
promptTemplate: ChatPromptTemplate = ChatPromptTemplate.from_template(template)
def formatTemplate(data: dict):
    return template, promptTemplate.invoke(data)

def upper(data: tuple):
    temp = data[0]
    formatedStr = data[1]
    print('Original Message is :', temp)
    print('Formatted message is :', formatedStr)

chain = RunnableLambda(formatTemplate) | RunnableLambda(upper)
chain.invoke({'variable1':'[variable1 value]', 'variable2':'[variable2 value]'})