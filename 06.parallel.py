from dotenv import *
from langchain_core.runnables import RunnableLambda, RunnableParallel

#load_dotenv()

def add(x: int):
    return x + x

def times(x: int):
    return x * x

addRunable = RunnableLambda(add)
timesRunable = RunnableLambda(times)

def mergeAnswer(response):
    addResult = response['funsCallingInTwoWay']['addFun']
    timesResult = response['funsCallingInTwoWay']['timesFun']
    return f'add result = {addResult}, times result = {timesResult}'

def printResult(msg: str):
    print(msg)

chain = RunnableParallel(funsCallingInTwoWay={'addFun': add, 'timesFun': times}) | mergeAnswer | printResult
chain.invoke(5)