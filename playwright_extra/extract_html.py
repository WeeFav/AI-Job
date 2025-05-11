from __future__ import annotations

from typing import Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from pydantic import BaseModel

from langchain_community.tools.playwright.base import BaseBrowserTool
from langchain_community.tools.playwright.utils import (
    aget_current_page,
    get_current_page,
)


class ExtractHTMLToolInput(BaseModel):
    """Explicit no-args input for ExtractHTMLTool."""


class ExtractHTMLTool(BaseBrowserTool):
    """Tool for extracting HTML on the current webpage."""

    name: str = "extract_html"
    description: str = "Extract HTML on the current webpage"
    args_schema: Type[BaseModel] = ExtractHTMLToolInput

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        if self.sync_browser is None:
            raise ValueError(f"Synchronous browser not provided to {self.name}")
        page = get_current_page(self.sync_browser)
        html_content = page.content()
        return html_content

    async def _arun(
        self,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        if self.async_browser is None:
            raise ValueError(f"Asynchronous browser not provided to {self.name}")
        page = await aget_current_page(self.async_browser)
        html_content = await page.content()
        return html_content
