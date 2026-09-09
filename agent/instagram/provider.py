from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable


@dataclass(slots=True)
class InstagramPost:
    id: str
    url: str
    caption: str = ""
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class InstagramComment:
    id: str
    post_id: str
    username: str
    text: str
    has_reply_from_page: bool = False
    metadata: dict[str, str] = field(default_factory=dict)


class InstagramProvider(ABC):
    """Adapter contract used by the agent core."""

    @abstractmethod
    def list_posts(self) -> Iterable[InstagramPost]:
        raise NotImplementedError

    @abstractmethod
    def list_comments(self, post: InstagramPost) -> Iterable[InstagramComment]:
        raise NotImplementedError

    @abstractmethod
    def reply_to_comment(self, comment: InstagramComment, text: str) -> None:
        raise NotImplementedError
