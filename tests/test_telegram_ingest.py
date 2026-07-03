from scappy_telegram.telegram_ingest import parse_channel_ref


def test_parse_channel_ref_converts_numeric_ids() -> None:
    assert parse_channel_ref("-100123456789") == -100123456789


def test_parse_channel_ref_keeps_usernames() -> None:
    assert parse_channel_ref("deals_channel") == "deals_channel"
