import pprint, time
import uuid
from common import *
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

start_time = time.time()  # 获取开始时间
load_dotenv()

# 每次运行生成一个 session_id，方便在 LangSmith 里按一次实验过滤
session_id = f"study-session-{uuid.uuid4()}"

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

config: RunnableConfig = {
    "run_name": "basic_chat_model_invoke",
    "tags": [
        "study",
        "langsmith-basic",
        "chatopenai",
        "test.py",
    ],
    "metadata": {
        "lesson": "basic_langsmith_observability",
        "stage": "01_single_llm_call",
        "environment": "local",
        "user_id": "vincent",
        "session_id": session_id,
        "input_type": "plain_text",
        "model_purpose": "simple_greeting_test",
    },
}


messages = [
    SystemMessage("你是一语言专家,精通英语和中文。用户将输入一个英文单词，你的回复是直接翻译该英文单词为中文"),
]

model = ChatOpenAI(model="gpt-4o-mini")

while True:
    user_input = input("> ")
    if user_input.lower() == "exit":
        break
    elif len(user_input.strip()) == 0:
        continue

    # 将用户消息加入数组
    messages.append(HumanMessage(user_input))

    # 调用模型
    result = model.invoke(messages, config=config)

    # 将模型返回的消息加入数组
    print("> " + result.content)
    messages.append(AIMessage(result.content))

print(evalEndTime(start_time))
pprint.pprint(messages)