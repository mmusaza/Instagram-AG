from agent.core.comment_analyzer import CommentIntent, analyze_comment


def test_empty_comment_is_ignored() -> None:
    result = analyze_comment("", False)
    assert result.needs_reply is False


def test_existing_reply_is_ignored() -> None:
    result = analyze_comment("سلام", True)
    assert result.needs_reply is False
    assert result.reason == "already answered"


def test_price_question_is_purchase_intent() -> None:
    result = analyze_comment("قیمت چنده؟", False)
    assert result.intent == CommentIntent.PURCHASE
    assert result.needs_reply is True


def test_link_comment_is_filtered_as_spam() -> None:
    result = analyze_comment("https://example.com", False)
    assert result.intent == CommentIntent.SPAM
    assert result.needs_reply is False


def test_positive_comment_can_receive_reply() -> None:
    result = analyze_comment("عالیه", False)
    assert result.intent == CommentIntent.POSITIVE
    assert result.needs_reply is True
