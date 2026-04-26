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

# :books: Youtube 视频处理

操作步骤

+ 处理视频字幕
+ 获取视频信息
+ 使用 YoutubeLoader 工具

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
    box-shadow: 2px 2px 3px black;
  }
</style>

![width:200px](./images/step-by-step-operation.webp)

# 操作演示

---
<style scoped>
  h3 {
    margin-top: 0;
  }
  pre {
    box-shadow: 2px 2px 3px black;
  }
</style>
## 课堂实验

### 执行脚本

```bash
pip install pytube==15.0.0 \
  youtube-transcript-api==0.6.2
```

---
<style scoped>
  h3 {
    margin-top: 0;
  }
  pre {
    box-shadow: 2px 2px 3px black;
  }
</style>
## 处理视频字幕

```python
from youtube_transcript_api import YouTubeTranscriptApi

# 视频ID
video_id = "iHrZKQQpuJQ"

# 列出可用字幕
transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
# print(transcript_list)

# 获取字幕
transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
# print(transcript)
content = ""
for item in transcript:
    # print(item['text'])
    if item['text'] != "[Music]":
        content += item['text'] + " "

print(content)

# 翻译字幕
transcript = transcript_list.find_transcript(['en'])
translated_transcript = transcript.translate('zh-Hans')

content = ""
for item in translated_transcript.fetch():
    if item['text'] != "[音乐]":
        content += item['text'] + ""
print(content)
```

---
<style scoped>
  h3 {
    margin-top: 0;
  }
  pre {
    box-shadow: 2px 2px 3px black;
  }
</style>
## 获取视频信息

```python
import pprint
from pytube import YouTube

video_id = "IBgWKTaG_Bs"
yt = YouTube(f"https://youtu.be/{video_id}")
# pprint.pprint(dir(yt))

print(yt.age_restricted)
print(yt.allow_oauth_cache)
print(yt.author)
print(yt.bypass_age_gate)
print(yt.caption_tracks)
print(yt.captions)
print(yt.channel_id)
print(yt.channel_url)
print(yt.check_availability)
print(yt.description)
# print(yt.embed_html)
print(yt.embed_url)
print(yt.from_id)
# print(yt.initial_data)
# print(yt.js)
print(yt.js_url)
print(yt.keywords)
print(yt.length)
print(yt.metadata)
print(yt.publish_date)
print(yt.rating)
print(yt.thumbnail_url)
print(yt.title)
print(yt.use_oauth)
# print(yt.vid_info)
print(yt.video_id)
print(yt.views)
print(yt.watch_url)
# print(yt.watch_html)
```

---
<style scoped>
  h3 {
    margin-top: 0;
  }
  pre {
    box-shadow: 2px 2px 3px black;
  }
</style>
## 使用 YoutubeLoader 工具

```python
from langchain_community.document_loaders import YoutubeLoader

print("=" * 100)

urls = [
    "https://www.youtube.com/watch?v=iHrZKQQpuJQ",
    "https://www.youtube.com/watch?v=UFjMfgBI82o",
]
docs = []
for url in urls:
    docs.extend(
        YoutubeLoader.from_youtube_url(
            url, add_video_info=True, translation="zh-Hans"
        ).load()
    )
doc = docs[0]
print(doc)

print("-" * 100)
print("标题:", doc.metadata["title"])
print("作者:", doc.metadata["author"])
print("发布:", doc.metadata["publish_date"])
print("图片:", doc.metadata["thumbnail_url"])
print("内容:", doc.page_content.replace("\n", ""))
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

