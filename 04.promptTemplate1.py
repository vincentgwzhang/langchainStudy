from pprint import pprint

from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompt_values import PromptValue

message = 'this is a variable1={variable1}, and this is a variable2={variable2}'
template: ChatPromptTemplate= ChatPromptTemplate.from_template(message)

value: PromptValue = template.invoke(
    {
        "variable1": "value for variable1", 
        "variable2": "value for variable2"
    }
)
print(value.messages[0].content)

################################################################################

'''
如果是 BaseMessage 子类实例，比如 SystemMessage、HumanMessage、AIMessage
LangChain 会认为它已经是“最终消息”，
不会再把里面的 {variable} 当模板变量替换。
'''
messages = [
    SystemMessage("message1"),
    HumanMessage("message2"),
    AIMessage('this is a variable1={variable1}, and this is a variable2={variable2}'),
    HumanMessage("message3"),
]

'''
只能使用模板形式
'''
messages = [
    ('system', 'message1'),
    ('human', 'message2'),
    ('ai', 'this is a variable1={variable1}, and this is a variable2={variable2}'),
    ('human', 'message3'),
]

template: ChatPromptTemplate= ChatPromptTemplate.from_messages(messages)
value: PromptValue = template.invoke(
    {
        "variable1": "value for variable1", 
        "variable2": "value for variable2"
    }
)

for message in value.messages:
    print(type(message), message.content)