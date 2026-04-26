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
    color: #ffb86c;
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
  img {
    border: 20px solid white;
    border-radius: 10%;
  }
</style>

![width:200px drop-shadow:0,5px,10px,rgba(f,f,f,.4)](./images/langchain.png)

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

# :books: 初始化开发环境

配置 LangChain 课程本地的 Python 3 开发环境。

1. 创建虚拟环境
1. 安装 LangChain 等依赖包
1. 编写 main.py 程序
1. 运行程序

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
### 执行脚本

```bash
$ python -V
$ python -m venv _pvenv_
$ source _pvenv_/bin/activate
$ python -m pip install --upgrade pip
# 安装库
$ pip install \
  langchain==0.2.14 \
  langchain-community==0.2.12 \
  langchain-aws==0.1.16 \
  langchain-openai==0.1.22 \
  langchainhub==0.1.21 \
  langgraph==0.2.34 \
  langchain-chroma==0.1.4 \
  wikipedia==1.4.0 \
  tavily-python==0.4.0 \
  python-dotenv==1.0.1

  # chromadb==0.5.5 \

# 生成环境文件
cat << EOF > .env
OPENAI_API_KEY=123
TAVILY_API_KEY=456
ANTHROPIC_API_KEY=789
GOOGLE_API_KEY=XYZ
EOF

# 编辑程序
$ nano common.py
$ nano main.py
# 运行程序
$ python main.py
```

---
<style scoped>
  h3 {
    margin-top: 0;
  }
</style>
### common.py

```python
import os
import time


def printENV():
    # 获取所有环境变量
    env_vars = os.environ
    # 打印所有环境变量
    for key, value in env_vars.items():
        if key in ["OPENAI_API_KEY", "TAVILY_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY"]:
            print(f"{key}: {value}")


def evalEndTime(start_time):
    end_time = time.time()  # 获取结束时间
    execution_time = "(程序运行时间：%.2f 秒)" % (
        end_time - start_time
    )  # 计算程序运行时间
    return execution_time
```

---
<style scoped>
  h3 {
    margin-top: 0;
  }
</style>
### main.py

```python
import os, pprint, json, time
from common import *
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

print("=" * 100)

start_time = time.time()  # 获取开始时间

load_dotenv()

printENV()

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

