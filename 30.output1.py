import os, pprint, json, time
from common import *
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import Optional
from pydantic import BaseModel, Field

print("=" * 100)
start_time = time.time()
load_dotenv()

# Pydantic
class Result(BaseModel):
    items: list[str] = Field()
    answer: str = Field()

llm = ChatOpenAI(model="gpt-4o-mini")
structured_llm = llm.with_structured_output(Result)

result = structured_llm.invoke("告诉我5个奥运会的项目")
print(result)