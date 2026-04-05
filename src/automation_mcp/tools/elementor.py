from automation_mcp.client import WordPressClient


async def get_elementor_info(site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("get-elementor-info", {})
