from langchain.tools import tool
from typing import List


class FallbackTool:
    def __init__(self):
        self.fallback_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        @tool
        def brute_force_language_list(_: str = "") -> str:
            """Return a concise statement about supported languages."""
            return (
                "I can understand and generate text in many languages. "
                "If you need a full language list, please ask for a specific region or subset."
            )

        return [brute_force_language_list]
