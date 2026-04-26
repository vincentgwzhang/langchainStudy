import time
from common import *
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableSequence

start_time = time.time()  # 获取开始时间
load_dotenv()

# 消息数组
print("=" * 100)
messages = [
    ("human", "我想学习{language}语言,请用英语回答我,并且控制在35个单词以内."),
]
prompt_template = ChatPromptTemplate.from_messages(messages)
# 大语言模型
# model = ChatBedrock(
#     credentials_profile_name="deeplearnaws",
#     region_name="us-east-1",
#     model_id="anthropic.claude-3-haiku-20240307-v1:0",
#     model_kwargs={
#         "max_tokens": 512,
#         "temperature": 0,
#         "top_p": 1.0,
#     },
# )

model = ChatOpenAI(model="gpt-4o-mini")

# 使用Chain调用模型
run_prompt = RunnableLambda(lambda x: prompt_template.invoke(x))
run_model = RunnableLambda(lambda x: model.invoke(x))
run_output = RunnableLambda(lambda x: StrOutputParser().invoke(x))
run_uppercase = RunnableLambda(lambda x: x.upper())  # 将输出转换为大写
run_countwords = RunnableLambda(lambda x: f"{x}\n>{len(x)}")  # 计算输出的单词数
# run_countwords = RunnableLambda(lambda x: print(x) or len(x))  # 计算输出的单词数

# chain = RunnableSequence(first=run_prompt, middle=[run_model], last=run_output)
#
# chain = run_prompt | run_model | run_output
# chain = run_prompt | run_model | run_output | run_uppercase
chain = run_prompt | run_model | run_output | run_uppercase | run_countwords
result = chain.invoke({"language": "python"})
print(result)

# 打印结束时间
print(evalEndTime(start_time))