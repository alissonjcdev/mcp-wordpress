import httpx
from pathlib import Path
from typing import Any

from automation_mcp.config import get_site_config, DEFAULT_CONFIG_PATH


class WordPressClient:
    def __init__(self, site_name: str | None = None, config_path: Path = DEFAULT_CONFIG_PATH):
        site = get_site_config(site_name, config_path)
        self.base_url = site["url"].rstrip("/")
        self.api_key = site["api_key"]
        self.endpoint = f"{self.base_url}/wp-json/automation-mcp/v1/execute"
        self.ping_endpoint = f"{self.base_url}/wp-json/automation-mcp/v1/ping"

    async def execute(self, action: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                self.endpoint,
                json={"action": action, "params": params or {}},
                headers={
                    "X-AMCP-Key": self.api_key,
                    "Content-Type": "application/json",
                },
            )
            data = response.json()

            if not data.get("success"):
                error = data.get("error", {})
                raise RuntimeError(
                    f"[{error.get('code', 'unknown')}] {error.get('message', 'Erro desconhecido')}"
                )

            return data

    async def ping(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                self.ping_endpoint,
                headers={"X-AMCP-Key": self.api_key},
            )
            return response.json()
