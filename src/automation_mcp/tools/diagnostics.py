from automation_mcp.client import WordPressClient


async def get_site_overview(site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("get-site-overview", {})


async def site_health(site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("site-health", {})


async def clear_cache(site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("clear-cache", {})


async def optimize_db(site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("optimize-db", {})
