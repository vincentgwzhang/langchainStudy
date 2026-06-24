import os, pprint, json, time
import uuid
from common import *
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

start_time = time.time()  # 获取开始时间
load_dotenv()

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

##############################################################################
messages = [
    SystemMessage("你是一位幽默大师，你的回答经常会让客户捧腹大笑。"),
    HumanMessage("你好"),
]
model = ChatOpenAI(model="gpt-4o-mini")
result = model.invoke(messages, config = config)
print(result.content)
##############################################################################
print()
print(evalEndTime(start_time))