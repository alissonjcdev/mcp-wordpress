import json
from pathlib import Path

from automation_mcp.config import load_config, save_config, get_site_config


def test_load_config_creates_default(tmp_path):
    config_path = tmp_path / "config.json"
    config = load_config(config_path)
    assert config["default_site"] == ""
    assert config["sites"] == {}
    assert config_path.exists()


def test_save_and_load_roundtrip(tmp_path):
    config_path = tmp_path / "config.json"
    config = {
        "default_site": "blog",
        "sites": {
            "blog": {
                "url": "https://blog.example.com",
                "api_key": "amcp_sk_test123",
                "label": "My Blog",
            }
        },
    }
    save_config(config, config_path)
    loaded = load_config(config_path)
    assert loaded["default_site"] == "blog"
    assert loaded["sites"]["blog"]["url"] == "https://blog.example.com"


def test_get_site_config_default(tmp_path):
    config_path = tmp_path / "config.json"
    config = {
        "default_site": "blog",
        "sites": {
            "blog": {"url": "https://blog.example.com", "api_key": "amcp_sk_123", "label": "Blog"},
            "shop": {"url": "https://shop.example.com", "api_key": "amcp_sk_456", "label": "Shop"},
        },
    }
    save_config(config, config_path)
    site = get_site_config(config_path=config_path)
    assert site["url"] == "https://blog.example.com"


def test_get_site_config_explicit(tmp_path):
    config_path = tmp_path / "config.json"
    config = {
        "default_site": "blog",
        "sites": {
            "blog": {"url": "https://blog.example.com", "api_key": "amcp_sk_123", "label": "Blog"},
            "shop": {"url": "https://shop.example.com", "api_key": "amcp_sk_456", "label": "Shop"},
        },
    }
    save_config(config, config_path)
    site = get_site_config(site_name="shop", config_path=config_path)
    assert site["url"] == "https://shop.example.com"


def test_get_site_config_not_found(tmp_path):
    config_path = tmp_path / "config.json"
    save_config({"default_site": "", "sites": {}}, config_path)
    try:
        get_site_config(site_name="nope", config_path=config_path)
        assert False, "Should have raised"
    except ValueError as e:
        assert "nope" in str(e)
