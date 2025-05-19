from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.tools.base import ArgsSchema
from .base import MyBaseBrowserTool
from langchain_community.tools.playwright.utils import aget_current_page
from bs4 import BeautifulSoup

class ExtractHTMLInput(BaseModel):
    """Explicit no-args input for ExtractHTMLTool."""
    
class ExtractHTMLTool(MyBaseBrowserTool):
    name: str = "extract_html"
    description: str = "Extract HTML on the current webpage"
    args_schema: Optional[ArgsSchema] = ExtractHTMLInput

    def _run(self) -> str:
        """Use the tool."""
        return "Not implemented"

    async def _arun(
        self,
    ) -> str:
        """Use the tool."""
        if self.async_browser is None:
            raise ValueError(f"Asynchronous browser not provided to {self.name}")
        page = await aget_current_page(self.async_browser)
        html_content = await page.content()
        return html_content