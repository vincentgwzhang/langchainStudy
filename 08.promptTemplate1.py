from langchain_core.prompts import ChatPromptTemplate

# 单参数
print("=" * 100)
template = "我想学习{language}语言，给我几个开发框架好吗？"
prompt_template = ChatPromptTemplate.from_template(template)

prompt = prompt_template.invoke({"language": "Python"})
print(prompt)
prompt = prompt_template.invoke({"language": "Java"})
print(prompt)
prompt = prompt_template.invoke({"language": "PHP"})
print(prompt)

# 多参数
print("=" * 100)
template = "我想学习{language}语言，给我几个开发{target}好吗？"
prompt_template = ChatPromptTemplate.from_template(template)

prompt = prompt_template.invoke({"language": "Python", "target": "框架"})
print(prompt)
prompt = prompt_template.invoke({"language": "Python", "target": "例子"})
print(prompt)

# 消息数组
print("=" * 100)
messages = [
    ("system", "你是一位{career}专家，你经常辅导你的学生。"),
    ("human", "我想学习{language}，给我几个建议好吗？"),
]
prompt_template = ChatPromptTemplate.from_messages(messages)
prompt = prompt_template.invoke({"career": "IT", "language": "Python"})
print(prompt)
prompt = prompt_template.invoke({"career": "医学", "language": "按摩"})
print(prompt)