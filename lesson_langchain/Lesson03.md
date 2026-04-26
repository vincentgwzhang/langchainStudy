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

# :books: 聊天模型

## LangChain 官方文档
https://python.langchain.com/v0.2/docs/integrations/chat/

---
<style scoped>
  section {
    font-size: 40px;
    align-items: center;
    justify-content: center;
  }
  table {
    font-family: Menlo;
  }
  th {
    font-family: Menlo;
    font-size: 42px;
    color: #3E4846;
  }
  tr {
    font-family: Menlo;
    font-size: 32px;
    color: #50716B;
  }
</style>
# 主要模型

| 模型接口                     | 说明                              |
|-----------------------------|----------------------------------|
| ChatOpenAI                  | OpenAI的聊天模型                  |
| ChatBedrock                 | Amazon的聊天模型                  |
| ChatGoogleGenerativeAI      | Google的生成式AI聊天模型          |
| ChatAnthropic               | Anthropic的聊天模型               |

+ Claude 3.x 模型可以在 Amazon Bedrock 上运行

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

