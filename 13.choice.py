import pprint

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    max_tokens=200,
)

mathQuestion = RunnableLambda(lambda x: x)

def formatQuestion(question):
    messages = [
        ('system', '你是个数学专家, 专门回答学生的数学问题'),
        ('human', '我想问你 {question}, 请你直接告诉我结果(你的答案应该是仅仅直接提供整数数值)')
    ]

    chatPromptTemplate = ChatPromptTemplate.from_messages(messages)
    return chatPromptTemplate.format_prompt(question = question)

handler1 = RunnableLambda(lambda x: 'x > 10')
handler2 = RunnableLambda(lambda x: 'x < 10')
handler3 = RunnableLambda(lambda x: 'x == 10')

def formatResult(x):
    return int(x)

branches = RunnableBranch(
    (lambda result: result > 10, handler1),
    (lambda result: result < 10, handler2),
    handler3
)

chain = mathQuestion | RunnableLambda(formatQuestion) | model | StrOutputParser() | RunnableLambda(formatResult) | branches
print(chain.invoke('10 + 0 等于几'))