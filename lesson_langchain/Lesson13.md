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
    font-family: Menlo;
    font-size: 32px;
  }
</style>

# :books: 分支思考处理(根据结果判断下一步操作)

操作步骤

+ 使用大语言模型判断用户输入的情绪，然后根据用户情绪进行下一步处理

---
<style scoped>
  h1 {
    font-size: 64px;
    color: #f8f8f2;
    margin: 0;
  }
  section {
    align-items: center;
    justify-content: center;
  }
  img {
    border-radius: 2%;
    margin-top: 20px;
    margin-bottom: 120px;
    border: 15px solid #f8f8f2;
    background-color: #f8f8f2 !important;
  }
</style>

# 系统架构

![width:800px](./images/Lesson13a.png)

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
from common import *
from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnableBranch

# 执行开始
print("=" * 100)
start_time = time.time()  # 获取开始时间
load_dotenv()

# 删除字符串中的所有空格
remove_spaces = lambda x: x.replace(" ", "")

# 客户输入
client_prompt = "这饭真难吃"
# client_prompt = "好累啊"
# client_prompt = "你是猪"
# client_prompt = "明天什么天气？"
print(client_prompt, "\n")

# 创建模型
model = ChatBedrock(
    credentials_profile_name="deeplearnaws",
    region_name="us-east-1",
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    model_kwargs={
        "max_tokens": 512,
        "temperature": 0,
        "top_p": 1.0,
    },
)


prompt_tpl = """
指令:请判断下面的`文本`是正面,负面还是中性的。

文本:这东西真难吃
结果:负面

文本:路太远啦
结果:负面

文本:今天心情不错
结果:正面

文本:时间太长了
结果:负面

文本:我们出发吧
结果:中性

文本:早睡早起
结果:中性

文本:{content}
结果:
"""


# 定义一位客服AI
def customer_service_ai(content):
    messages = [
        (
            "system",
            """你是一位客户人员，你需要判断客户的情绪是正面、负面还是中性。""",
        ),
        ("human", prompt_tpl.format(content=content)),
    ]
    prompt_template = ChatPromptTemplate.from_messages(messages)
    return prompt_template.format_prompt(content=content)


prompt_input_chain = RunnableLambda(lambda input: customer_service_ai(input))


# 整理情绪
def emotion_parser(emotion):
    # print(">>", emotion)
    if "结果:正面" in remove_spaces(emotion):
        return "正面"
    elif "结果:负面" in remove_spaces(emotion):
        return "负面"
    else:
        return "中性"


emotion_parser_chain = RunnableLambda(lambda x: emotion_parser(x))


# 正面处理(Positive)
positive_chain = RunnableLambda(lambda x: "[ACTION]正面处理(Positive)")

# 负面处理(Negative)
negative_chain = RunnableLambda(lambda x: "[ACTION]负面处理(Negative)")

# 中性处理(Neutral)
neutral_chain = RunnableLambda(lambda x: "[ACTION]中性处理(Neutral)")


# 分支思考
branches = RunnableBranch(
    (lambda x: x == "正面", positive_chain),
    (lambda x: x == "负面", negative_chain),
    neutral_chain,
)


# 输出过程中的数据
def output(x):
    print(">", x)
    return x


output_chain = RunnableLambda(lambda x: output(x))

# 定义Chain
chain = (
    prompt_input_chain
    | model
    | StrOutputParser()
    | output_chain
    | emotion_parser_chain
    | output_chain
    | branches
    | output_chain
)
result = chain.invoke(client_prompt)
print()

# 打印结束时间
print(evalEndTime(start_time))
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

