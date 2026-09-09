from __future__ import annotations

from pathlib import Path
from playwright.sync_api import BrowserContext, Page, sync_playwright


class InstagramBrowser:
    """Persistent Playwright session. Login is intentionally manual."""

    def __init__(self, headless: bool = False, session_dir: str = "data/instagram-session") -> None:
        self.headless = headless
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self._playwright = None
        self._context: BrowserContext | None = None

    def start(self) -> Page:
        self._playwright = sync_playwright().start()
        self._context = self._playwright.chromium.launch_persistent_context(
            str(self.session_dir),
            headless=self.headless,
            viewport={"width": 1440, "height": 900},
        )
        return self._context.pages[0] if self._context.pages else self._context.new_page()

    def stop(self) -> None:
        if self._context:
            self._context.close()
        if self._playwright:
            self._playwright.stop()
