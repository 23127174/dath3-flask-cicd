from app import app


def test_home():
    c = app.test_client()
    r = c.get("/")
    assert r.status_code == 200
    assert b"DATH#3 - CI/CD" in r.data


def test_health():
    c = app.test_client()
    r = c.get("/health")
    assert r.status_code == 200
    assert r.json["status"] == "ok"
