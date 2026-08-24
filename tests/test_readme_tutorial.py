from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_is_an_indonesian_deployment_and_identity_tutorial():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for marker in (
        "docs/assets/technocore-key.gif",
        "## Tutorial penggunaan",
        "## Deploy ke Vercel",
        "Generate identity",
        "Sign with active DID",
        "Forget from tab",
        "python scripts/build_vercel.py",
    ):
        assert marker in readme


def test_readme_banner_is_a_real_looping_gif():
    animation = (ROOT / "docs" / "assets" / "technocore-key.gif").read_bytes()
    assert animation.startswith((b"GIF87a", b"GIF89a"))
    assert animation.count(b"\x21\xf9\x04") >= 10  # graphic-control blocks, one per frame
    assert b"NETSCAPE2.0" in animation  # loop extension
    assert len(animation) < 3 * 1024 * 1024
