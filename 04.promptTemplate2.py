from pprint import pprint

from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompt_values import PromptValue
from langchain_openai import ChatOpenAI
from dotenv import *

load_dotenv()

questionTemplate = '请直接回复{expression} 等于多少'

template: ChatPromptTemplate = ChatPromptTemplate.from_template(questionTemplate)
value: PromptValue = template.invoke({'expression': '1+1'})

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens = 32
)

message: AIMessage = model.invoke(value)
print(message.content)