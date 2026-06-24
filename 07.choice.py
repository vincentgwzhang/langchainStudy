import pprint

from dotenv import *
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel

def printWhenInputLessThan10(val: int):
    print(f'The input value {val} is less than 10')

def printWhenInputMoreThan10(val: int):
    print(f'The input value {val} is more than 10')

def printWhenInputEqualsTo10(val: int):
    print(f'The input value {val} is equals to 10')

makeChoice = RunnableBranch(
    (lambda x: x < 10, RunnableLambda(printWhenInputLessThan10)),
    (lambda x: x > 10, RunnableLambda(printWhenInputMoreThan10)),
    RunnableLambda(printWhenInputEqualsTo10)
)

chain = RunnableLambda(lambda x : x['val']) | makeChoice
chain.invoke({'val': 20})