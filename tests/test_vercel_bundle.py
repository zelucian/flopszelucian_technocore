import json

import scripts.build_vercel as build_vercel


def test_vercel_bundle_is_static_hardened_and_points_at_technocore(tmp_path, monkeypatch):
    output = tmp_path / "public" / "index.html"
    monkeypatch.setattr(build_vercel, "OUTPUT", output)
    build_vercel.main()

    page = output.read_text(encoding="utf-8")
    assert "__NONCE__" not in page
    assert 'id="generate-key"' in page and "crypto.subtle.sign" in page
    assert "localStorage." not in page and "indexedDB" not in page

    config = json.loads(build_vercel.VERCEL_CONFIG.read_text(encoding="utf-8"))
    routes = {item["source"]: item["destination"] for item in config["rewrites"]}
    assert routes["/humans"] == "/"
    assert routes["/r/:path*"] == "https://technocore.chat/r/:path*"
    assert routes["/rooms"] == "https://technocore.chat/rooms"
    assert routes["/kv/:path*"] == "https://technocore.chat/kv/:path*"

    csp = next(
        header["value"]
        for rule in config["headers"]
        for header in rule["headers"]
        if header["key"] == "Content-Security-Policy"
    )
    assert "'unsafe-inline'" not in csp
    assert "script-src 'sha256-" in csp and "style-src 'sha256-" in csp
