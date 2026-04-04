from automation_mcp.client import WordPressClient


async def list_themes(site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("list-themes", {})


async def install_theme(slug: str, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("install-theme", {"slug": slug})


async def activate_theme(slug: str, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("activate-theme", {"slug": slug})


async def customize_theme(settings: dict, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("customize-theme", {"settings": settings})
