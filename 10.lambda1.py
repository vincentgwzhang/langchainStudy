from langchain_core.runnables import RunnableLambda

# RunnableLambda 允许将一个任意的Python函数包装成一个可以在LangChain框架中运行的组件。主要用于定义自定义的任务或操作，这些任务可以在你的语言链中作为一个节点执行。
# 字母大写
def to_uppercase(inputs):
    return inputs.upper()

# 前后加括号
def append_comma(inputs):
    return f"[[[{inputs}]]]"


to_uppercase_lambda = RunnableLambda(to_uppercase)
append_comma_lambda = RunnableLambda(append_comma)

chain = to_uppercase_lambda | append_comma_lambda
print(chain.invoke("hello world"))