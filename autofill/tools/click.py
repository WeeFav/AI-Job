from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.tools.base import ArgsSchema
from .base import MyBaseBrowserTool
from langchain_community.tools.playwright.utils import aget_current_page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

class ClickInput(BaseModel):
    selector: str = Field(description="CSS selector for the element to click")
    
class ClickTool(MyBaseBrowserTool):
    name: str = "click"
    description: str = "Click on an element with the given CSS selector"
    args_schema: Optional[ArgsSchema] = ClickInput

    def _run(self) -> str:
        """Use the tool."""
        return "Not implemented"

    async def _arun(
        self,
        selector: str,
    ) -> str:
        """Use the tool."""
        if self.async_browser is None:
            raise ValueError(f"Asynchronous browser not provided to {self.name}")
        page = await aget_current_page(self.async_browser)
        
        try:
            await page.click(
                selector,
                timeout=10000, # 10 seconds
            )
        except PlaywrightTimeoutError:
            return f"Unable to click on element '{selector}'"
        return f"Clicked element '{selector}'"
