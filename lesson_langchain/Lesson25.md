---
marp: true
theme: default
header: 'LangChain AI开发课程'
footer: '小马技术'
style: |
  header {
    color: #00ced1;
    font-weight: bold;
  }
  footer {
    color: #50fa7b;
    font-weight: bold;
  }
  h1 {
    color: #f8f8f2;
    font-size: 64px;
  }
  section {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    background-color: #1d3d3c;
    color: #f8f8f2;
    font-size: 24px;
    font-family: Yuanti SC;
  }
  a {
    color: #8be9fd;
  }
  img {
    background-color: transparent!important;
  }
  code {
    font-family: JetBrains Mono;
  }

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
  h1 {
    color: #f8f8f2;
    font-size: 120px;
  }
</style>

![width:300px drop-shadow:0,5px,10px,rgba(f,f,f,.4)](./images/langchain.png)

# LangChain

---
<style scoped>
  section {
    font-size: 40px;
  }
  h1 {
    font-size: 50px;
    color: #f8f8f2;
  }
  li {
    font-family: JetBrains Mono;
    font-size: 32px;
  }
</style>

# :books: 自定义工具

操作步骤

+ 自定义工具
+ 手动调用工具

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
  h1 {
    color: #f8f8f2;
    font-size: 200px;
    margin: 0;
  }
  img {
    border: 10px solid #f8f8f2;
    border-radius: 20%;
    margin: 0;
  }
</style>

![width:200px](./images/step-by-step-operation.webp)

# 操作演示

---
<style scoped>
  h3 {
    margin-top: 0;
  }
</style>
### main.py

```python
import time
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import StructuredTool
from common import *

print("=" * 100)


start_time = time.time()  # 获取开始时间


class SayHelloInput(BaseModel):
    name: str = Field(..., title="The name of the person to say hello to")


def say_hello(name: str) -> str:
    """
    Say hello to a person
    """
    return f"亲爱的{name}，你好!"


class ReverseStringInput(BaseModel):
    content: str = Field(..., title="The string to reverse")


def reverse_string(content: str) -> str:
    """
    Reverse a string
    """
    return content[::-1]


class ConcatenateStringsInput(BaseModel):
    a: str = Field(..., title="The first string")
    b: str = Field(..., title="The second string")


def concatenate_strings(a: str, b: str) -> str:
    """
    Concatenate two strings
    """
    return a + b


tools = [
    StructuredTool.from_function(
        func=say_hello,
        args_schema=SayHelloInput,
        output_field_name="greeting",
        description="Say hello to a person",
    ),
    StructuredTool.from_function(
        func=reverse_string,
        args_schema=ReverseStringInput,
        output_field_name="reversed_string",
        description="Reverse a string",
    ),
    StructuredTool.from_function(
        func=concatenate_strings,
        args_schema=ConcatenateStringsInput,
        output_field_name="result_string",
        description="Concatenate two strings",
    ),
]

# 直接调用工具
# print(tools[0].func("Koma"))
# print(tools[1].func("Hello"))
# print(tools[2].func("Hello", "World"))

# print(tools[0].invoke("Koma"))
# print(tools[1].invoke("Hello"))
# print(tools[2].invoke({"a": "Hello", "b": "World"}))

###############################################################################
# 打印结束时间
print("\n", evalEndTime(start_time))
```

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
  h1 {
    color: #f8f8f2;
    font-size: 200px;
  }
</style>

# 下课时间

