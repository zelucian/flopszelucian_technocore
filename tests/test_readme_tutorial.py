from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_is_an_english_identity_and_signed_chat_tutorial():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for marker in (
        "docs/assets/technocore-key.gif",
        "## Guided tutorial",
        "docs/screenshots/01-generate-identity.jpg",
        "docs/screenshots/02-rooms-and-chat.jpg",
        "docs/screenshots/03-signed-chat.jpg",
        "<details open>",
        "Generate a seed and DID key",
        "Send a signed message",
        "Generate identity",
        "Sign with active DID",
        "Forget from tab",
        "room|nonce|text",
    ):
        assert marker in readme
    assert "## Deploy ke Vercel" not in readme


def test_readme_screenshots_are_real_jpeg_images():
    for name in (
        "01-generate-identity.jpg",
        "02-rooms-and-chat.jpg",
        "03-signed-chat.jpg",
    ):
        screenshot = (ROOT / "docs" / "screenshots" / name).read_bytes()
        assert screenshot.startswith(b"\xff\xd8\xff")
        assert screenshot.endswith(b"\xff\xd9")
        assert len(screenshot) >= 40_000


def test_readme_banner_is_a_real_looping_gif():
    animation = (ROOT / "docs" / "assets" / "technocore-key.gif").read_bytes()
    assert animation.startswith((b"GIF87a", b"GIF89a"))
    assert animation.count(b"\x21\xf9\x04") >= 10  # graphic-control blocks, one per frame
    assert b"NETSCAPE2.0" in animation  # loop extension
    assert len(animation) < 3 * 1024 * 1024
