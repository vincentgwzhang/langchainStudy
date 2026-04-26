import os
import shutil
import time
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

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

def empty_folder(folder_path: str):
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"{folder_path} does not exist")

    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"{folder_path} is not a directory")

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # 删除文件或符号链接
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # 递归删除子目录
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")

class StructureAIMessage(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    content: str
    additional_kwargs: Dict[str, Any] = {}
    response_metadata: Dict[str, Any] = {}
    id: Optional[str] = None
    tool_calls: List[Any] = []
    invalid_tool_calls: List[Any] = []
    usage_metadata: Optional[Dict[str, Any]] = None