import json
import pytest
import httpx
import respx
from automation_mcp.client import WordPressClient


@pytest.fixture
def mock_config(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({
        "default_site": "test",
        "sites": {
            "test": {
                "url": "https://test.example.com",
                "api_key": "amcp_sk_test",
                "label": "Test",
            }
        },
    }))
    return config_path


@pytest.mark.asyncio
@respx.mock
async def test_execute_success(mock_config):
    respx.post("https://test.example.com/wp-json/automation-mcp/v1/execute").respond(
        json={"success": True, "data": {"post_id": 1}, "log_id": 1}
    )
    client = WordPressClient(config_path=mock_config)
    result = await client.execute("create-post", {"title": "Test"})
    assert result["success"] is True
    assert result["data"]["post_id"] == 1


@pytest.mark.asyncio
@respx.mock
async def test_execute_error(mock_config):
    respx.post("https://test.example.com/wp-json/automation-mcp/v1/execute").respond(
        json={"success": False, "error": {"code": "ability_disabled", "message": "Not allowed"}}
    )
    client = WordPressClient(config_path=mock_config)
    with pytest.raises(RuntimeError, match="Not allowed"):
        await client.execute("execute-php", {"code": "echo 1;"})


@pytest.mark.asyncio
@respx.mock
async def test_ping(mock_config):
    respx.get("https://test.example.com/wp-json/automation-mcp/v1/ping").respond(
        json={"success": True, "data": {"plugin_version": "1.0.0", "wp_version": "6.7"}}
    )
    client = WordPressClient(config_path=mock_config)
    result = await client.ping()
    assert result["data"]["plugin_version"] == "1.0.0"
