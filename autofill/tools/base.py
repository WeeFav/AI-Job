from typing import Optional
from langchain_core.tools import BaseTool
from playwright.async_api import Browser as AsyncBrowser

class MyBaseBrowserTool(BaseTool):
    """Base class for browser tools."""
    async_browser: Optional[AsyncBrowser] = None
    
    @classmethod
    def from_browser(cls, async_browser):
        return cls(async_browser=async_browser)