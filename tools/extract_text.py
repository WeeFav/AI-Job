from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.tools.base import ArgsSchema
from .base import MyBaseBrowserTool
from langchain_community.tools.playwright.utils import aget_current_page
from bs4 import BeautifulSoup

class ExtractTextInput(BaseModel):
    """Explicit no-args input for ExtractTextTool."""
    
class ExtractTextTool(MyBaseBrowserTool):
    name: str = "extract_text"
    description: str = "Extract all the text on the current webpage"
    args_schema: Optional[ArgsSchema] = ExtractTextInput

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

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, "lxml")

        return " ".join(text for text in soup.stripped_strings)
