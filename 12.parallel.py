import pprint

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    max_tokens=200,
)

formatLanguage = RunnableLambda(lambda x: '{language}'.format(language = x['language']))


def getPositivePromptValue(language):
    messages = [
        ('system', '你是一个程序专家'),
        ('human', '你是一个{career}, 请描述他比Java 好的地方')
    ]

    chatPromptTemplate = ChatPromptTemplate.from_messages(messages)
    return chatPromptTemplate.format_prompt(career = language)

positiveChain = RunnableLambda(lambda x: getPositivePromptValue(x)) | model | StrOutputParser()


def getNegativePromptValue(language):
    messages = [
        ('system', '你是一个程序专家'),
        ('human', '你是一个{career}, 请描述他比Java 差的地方')
    ]

    chatPromptTemplate = ChatPromptTemplate.from_messages(messages)
    return chatPromptTemplate.format_prompt(career = language)

negativeChain = RunnableLambda(lambda x: getNegativePromptValue(x)) | model | StrOutputParser()
# 运行RunnableParaller

# test area
def output(x):
    print(x)
    return x

def merge_answers(response):
    goodPoint = response['branches']['positive']
    badPoint = response['branches']['negative']
    return f'好处: {goodPoint} \n ********************************** \n坏处:{badPoint}'

chain = formatLanguage | RunnableParallel(branches={'positive': positiveChain, 'negative': negativeChain}) | merge_answers
finalResult = chain.invoke({'language': 'Python'})
print(finalResult)
# 结合在一起

# 打印出来