from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from playwright.sync_api import BrowserContext, Page, TimeoutError as PlaywrightTimeoutError, sync_playwright


class BrowserSession:
    """Persistent Playwright session for manual Instagram login.

    The browser profile is stored outside the repository. The first run can
    be logged in manually; later runs reuse the same session when Instagram
    permits it.
    """

    def __init__(self) -> None:
        self.profile_dir = Path(os.getenv("INSTAGRAM_PROFILE_DIR", "runtime/browser-profile"))
        self.headless = os.getenv("BROWSER_HEADLESS", "false").lower() == "true"
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        self._playwright: Any = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None

    def start(self) -> Page:
        self._playwright = sync_playwright().start()
        self.context = self._playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.profile_dir),
            headless=self.headless,
            viewport={"width": 1440, "height": 1000},
        )
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        self.page.goto("https://www.instagram.com/", wait_until="domcontentloaded")
        return self.page

    def ensure_login(self, timeout_ms: int = 120_000) -> None:
        if self.page is None:
            raise RuntimeError("Browser session has not been started")

        self.page.goto("https://www.instagram.com/", wait_until="domcontentloaded")
        try:
            self.page.wait_for_selector("svg[aria-label='Home']", timeout=5_000)
            return
        except PlaywrightTimeoutError:
            pass

        print("Instagram login is required. Complete login in the browser window.")
        print("After login, return here; the agent will continue automatically.")
        self.page.wait_for_timeout(2_000)
        self.page.wait_for_function(
            "() => document.querySelector(\"svg[aria-label='Home']\") !== null",
            timeout=timeout_ms,
        )

    def close(self) -> None:
        if self.context is not None:
            self.context.close()
        if self._playwright is not None:
            self._playwright.stop()
        self.context = None
        self.page = None
        self._playwright = None
