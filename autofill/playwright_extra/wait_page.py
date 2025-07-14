from __future__ import annotations

from typing import Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from pydantic import BaseModel

import time

from langchain_community.tools.playwright.base import BaseBrowserTool
from langchain_community.tools.playwright.utils import (
    aget_current_page,
    get_current_page,
)


class WaitWebPageToolInput(BaseModel):
    """Explicit no-args input for WaitWebPageTool."""


class WaitWebPageTool(BaseBrowserTool):
    """Tool for waiting for the webpage to load."""

    name: str = "wait_page"
    description: str = "Wait for the current page to fully load"
    args_schema: Type[BaseModel] = WaitWebPageToolInput

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        if self.sync_browser is None:
            raise ValueError(f"Synchronous browser not provided to {self.name}")
        # page = get_current_page(self.sync_browser)
        # page.wait_for_load_state("networkidle")
        time.sleep(5)

    async def _arun(
        self,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        if self.async_browser is None:
            raise ValueError(f"Asynchronous browser not provided to {self.name}")
        page = await aget_current_page(self.async_browser)
        await page.wait_for_load_state("networkidle")
