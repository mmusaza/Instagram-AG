from __future__ import annotations

import re
from urllib.parse import urljoin

from playwright.sync_api import Locator, Page

from agent.instagram.browser import BrowserSession
from agent.instagram.provider import InstagramComment, InstagramPost, InstagramProvider


_POST_RE = re.compile(r"^/p/[^/?#]+/?$")


class PlaywrightInstagramProvider(InstagramProvider):
    """Experimental browser provider.

    Instagram's UI is dynamic, so selectors are deliberately centralized in
    this module. Discovery is conservative: if a selector cannot be found,
    the provider returns what it can rather than making assumptions.
    """

    def __init__(self, session: BrowserSession, username: str, auto_reply: bool = False) -> None:
        self.session = session
        self.username = username.lstrip("@").strip()
        self.auto_reply = auto_reply

    @property
    def page(self) -> Page:
        if self.session.page is None:
            raise RuntimeError("Browser session is not started")
        return self.session.page

    def list_posts(self) -> list[InstagramPost]:
        self.page.goto(f"https://www.instagram.com/{self.username}/", wait_until="domcontentloaded")
        self.page.wait_for_timeout(2_000)

        links = self.page.locator("a[href]")
        seen: set[str] = set()
        posts: list[InstagramPost] = []
        for i in range(min(links.count(), 500)):
            href = links.nth(i).get_attribute("href") or ""
            if not _POST_RE.match(href):
                continue
            url = urljoin("https://www.instagram.com", href)
            if url in seen:
                continue
            seen.add(url)
            post_id = href.strip("/").split("/")[-1]
            posts.append(InstagramPost(id=post_id, url=url))
        return posts

    def list_comments(self, post: InstagramPost) -> list[InstagramComment]:
        self.page.goto(post.url, wait_until="domcontentloaded")
        self.page.wait_for_timeout(2_000)
        self._expand_comments()

        comments: list[InstagramComment] = []
        seen: set[str] = set()
        # Instagram changes markup frequently. We first collect comment-like
        # list items and only accept entries with a username + visible text.
        items = self.page.locator("ul li")
        for i in range(min(items.count(), 1000)):
            item = items.nth(i)
            parsed = self._parse_comment(item, post.id, i)
            if parsed is None or parsed.id in seen:
                continue
            seen.add(parsed.id)
            comments.append(parsed)
        return comments

    def reply_to_comment(self, comment: InstagramComment, text: str) -> None:
        if not self.auto_reply:
            return
        # Sending is intentionally isolated here. The first production tests
        # should run with auto_reply=False and inspect the generated actions.
        raise NotImplementedError(
            "Live reply submission is disabled until the test-account DOM flow is validated."
        )

    def _expand_comments(self) -> None:
        labels = (
            "View all comments",
            "View more comments",
            "Load more comments",
        )
        for label in labels:
            try:
                self.page.get_by_text(label, exact=False).first.click(timeout=1_500)
                self.page.wait_for_timeout(1_000)
            except Exception:
                continue

    def _parse_comment(self, item: Locator, post_id: str, index: int) -> InstagramComment | None:
        text = " ".join(item.inner_text().split()).strip()
        if len(text) < 2:
            return None

        links = item.locator("a[href]")
        username = ""
        for j in range(min(links.count(), 5)):
            href = links.nth(j).get_attribute("href") or ""
            if href.startswith("/") and "/" not in href.strip("/"):
                username = href.strip("/")
                break
        if not username:
            return None

        # Remove obvious action labels from the candidate text.
        for token in ("Reply", "Like", "Liked", "Follow"):
            text = text.replace(token, " ")
        text = " ".join(text.split()).strip()
        if len(text) < 2:
            return None

        has_reply = self._has_page_reply(item)
        return InstagramComment(
            id=f"{post_id}:{username}:{index}",
            post_id=post_id,
            username=username,
            text=text,
            has_reply_from_page=has_reply,
            metadata={"source": "playwright"},
        )

    def _has_page_reply(self, item: Locator) -> bool:
        # This is intentionally conservative. A reliable page-identity signal
        # should be supplied once we validate the test account's actual DOM.
        return False
