from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.tools.base import ArgsSchema
from .base import MyBaseBrowserTool
from langchain_community.tools.playwright.utils import aget_current_page
    
class NavigateInput(BaseModel):
    url: str = Field(description="url to navigate to")

class NavigateTool(MyBaseBrowserTool):
    name: str = "navigate"
    description: str = "Navigate a browser to the specified URL"
    args_schema: Optional[ArgsSchema] = NavigateInput

    def _run(self) -> str:
        """Use the tool."""
        return "Not implemented"

    async def _arun(
        self,
        url: str,
    ) -> str:
        """Use the tool."""
        if self.async_browser is None:
            raise ValueError(f"Asynchronous browser not provided to {self.name}")
        page = await aget_current_page(self.async_browser)
        response = await page.goto(url)
        status = response.status if response else "unknown"
        return f"Navigating to {url} returned status code {status}"
