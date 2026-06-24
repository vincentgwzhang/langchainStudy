"""
Small compatibility helper for reading these examples directly from this folder.
用于直接阅读/运行这些示例的小辅助文件。

中文：真实企业项目会把这些文件放进正式 Python package，例如 `app.rag.*`。
English: A real enterprise project would put these files into a proper Python package, such as `app.rag.*`.
"""

from __future__ import annotations

from pathlib import Path


def explain_import_note(folder: Path) -> str:
    return (
        f"Examples live in {folder}. "
        "For production, move them into a package and use absolute imports. "
        "中文：生产环境应放入正式 package，并使用绝对导入。"
    )
