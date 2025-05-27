from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_core.tools.base import ArgsSchema
from .base import MyBaseBrowserTool
from langchain_community.tools.playwright.utils import aget_current_page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

class FillInput(BaseModel):
    selectors: List[str] = Field(description="A list of CSS selectors for each element to fill")
    values: List[str] = Field(description="A list of text to be filled in each element")
    
class FillTool(MyBaseBrowserTool):
    name: str = "fill"
    description: str = "Fill on multiple elements with the given CSS selector"
    args_schema: Optional[ArgsSchema] = FillInput

    def _run(self) -> str:
        """Use the tool."""
        return "Not implemented"

    async def _arun(
        self,
        selectors: List[str],
        values: List[str],
    ) -> str:
        """Use the tool."""
        if self.async_browser is None:
            raise ValueError(f"Asynchronous browser not provided to {self.name}")
        page = await aget_current_page(self.async_browser)
        
        timeout_elements = []
        success_elements = []
        for i in range(len(selectors)):
            sel = selectors[i]
            val = values[i]
        
            try:
                await page.fill(
                    sel,
                    val,
                    timeout=3000, # 3 seconds
                )
                success_elements.append(sel)
            except PlaywrightTimeoutError:
                timeout_elements.append(sel)
        
        respond = ""
        if timeout_elements:
            te = ", ".join(timeout_elements)
            respond += f"Unable to fill on element(s) '{te}'. \n"
        if success_elements:
            se = ", ".join(success_elements)
            respond += f"Filled element(s) '{se}'."
        
        return respond
        
        