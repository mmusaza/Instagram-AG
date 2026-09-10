from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from playwright.sync_api import BrowserContext, Page, TimeoutError as PlaywrightTimeoutError, sync_playwright


class BrowserSession:
    """Persistent Playwright session using the locally installed Chrome browser.

    The first run can be logged in manually. The isolated profile is stored
    outside the repository and reused on later runs.
    """

    def __init__(self) -> None:
        self.profile_dir = Path(os.getenv("INSTAGRAM_PROFILE_DIR", "runtime/browser-profile"))
        self.chrome_path = os.getenv(
            "CHROME_EXECUTABLE_PATH",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        )
        self.headless = os.getenv("BROWSER_HEADLESS", "false").strip().lower() == "true"
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        self._playwright: Any = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None

    def start(self) -> Page:
        self._playwright = sync_playwright().start()

        launch_args: dict[str, Any] = {
            "user_data_dir": str(self.profile_dir),
            "headless": self.headless,
            "viewport": {"width": 1440, "height": 1000},
        }

        if Path(self.chrome_path).exists():
            launch_args["executable_path"] = self.chrome_path
        else:
            # If the configured Chrome path is unavailable, let Playwright use
            # its normal browser resolution. This gives a useful error if the
            # browser binary is not installed.
            launch_args["channel"] = "chrome"

        self.context = self._playwright.chromium.launch_persistent_context(**launch_args)
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        self.page.goto("https://www.instagram.com/", wait_until="domcontentloaded")
        return self.page

    def ensure_login(self, timeout_ms: int = 120_000) -> None:
        if self.page is None:
            raise RuntimeError("Browser session has not been started")

        self.page.goto("https://www.instagram.com/", wait_until="domcontentloaded")
        if self._looks_logged_in():
            print("Instagram session is already logged in.")
            return

        print("Instagram login is required. Complete login in the browser window.")
        print("After login, the agent will continue automatically.")

        self.page.wait_for_function(
            """() => {
                const text = document.body?.innerText || '';
                return Boolean(
                    document.querySelector('a[href*="/direct/"]') ||
                    document.querySelector('a[href*="/accounts/edit/"]') ||
                    /Home|خانه|Direct|پیام/i.test(text)
                );
            }""",
            timeout=timeout_ms,
        )

    def _looks_logged_in(self) -> bool:
        if self.page is None:
            return False
        try:
            return self.page.locator(
                'a[href*="/direct/"], a[href*="/accounts/edit/"]'
            ).count() > 0
        except PlaywrightTimeoutError:
            return False
        except Exception:
            return False

    def close(self) -> None:
        if self.context is not None:
            self.context.close()
        if self._playwright is not None:
            self._playwright.stop()
        self.context = None
        self.page = None
        self._playwright = None
