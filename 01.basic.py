import pprint
import time
import uuid
from dotenv import load_dotenv

from langchain.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig

import common

load_dotenv()

startTime = time.time()

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

user_input = "hello"

message: AIMessage = model.invoke(
    user_input,
    config=config,
)

pprint.pprint(message)

print("\n========== CONTENT ==========")
print(message.content)

print("\n========== RESPONSE METADATA ==========")
pprint.pprint(message.response_metadata)

print("\n========== USAGE METADATA ==========")
pprint.pprint(message.usage_metadata)

print("\n========== OBSERVABILITY SUMMARY ==========")

token_usage = message.response_metadata.get("token_usage", {})
usage_metadata = message.usage_metadata or {}

observability_summary = {
    "session_id": session_id,
    "model_name": message.response_metadata.get("model_name"),
    "model_provider": message.response_metadata.get("model_provider"),
    "finish_reason": message.response_metadata.get("finish_reason"),
    "service_tier": message.response_metadata.get("service_tier"),
    "system_fingerprint": message.response_metadata.get("system_fingerprint"),

    "prompt_tokens": token_usage.get("prompt_tokens"),
    "completion_tokens": token_usage.get("completion_tokens"),
    "total_tokens": token_usage.get("total_tokens"),

    "input_tokens": usage_metadata.get("input_tokens"),
    "output_tokens": usage_metadata.get("output_tokens"),

    "reasoning_tokens": usage_metadata
        .get("output_token_details", {})
        .get("reasoning"),

    "cache_read_tokens": usage_metadata
        .get("input_token_details", {})
        .get("cache_read"),

    "content_length": len(message.content or ""),
    "tool_call_count": len(message.tool_calls or []),
    "invalid_tool_call_count": len(message.invalid_tool_calls or []),
}

pprint.pprint(observability_summary)

common.evalEndTime(startTime)