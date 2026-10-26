import importlib
import os

from app.skill_engine import normalize_skill_name


def test_normalize_skill_name_handles_common_variants():
    assert normalize_skill_name(" python ") == "Python"
    assert normalize_skill_name("js") == "JavaScript"
    assert normalize_skill_name("Git/GitHub") == "Git"
    assert normalize_skill_name(" machine learning ") == "Machine Learning"


def test_main_config_uses_safe_defaults(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("FLASK_ENV", raising=False)
    monkeypatch.delenv("SESSION_COOKIE_SECURE", raising=False)

    import run
    importlib.reload(run)

    assert run.app.config["SECRET_KEY"]
    assert len(run.app.config["SECRET_KEY"]) >= 16
    assert run.app.config["SESSION_COOKIE_SAMESITE"] == "Lax"
    assert run.app.config["SESSION_COOKIE_SECURE"] is False


def test_main_bool_env_parser_accepts_truthy_values():
    import run

    assert run._get_bool_env("TRUE", False) is True
    assert run._get_bool_env("1", False) is True
    assert run._get_bool_env("yes", False) is True
    assert run._get_bool_env("off", False) is False
