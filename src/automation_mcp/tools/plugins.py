from automation_mcp.client import WordPressClient


async def list_plugins(site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("list-plugins", {})


async def install_plugin(slug: str, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("install-plugin", {"slug": slug})


async def activate_plugin(plugin: str, deactivate: bool = False, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("activate-plugin", {"plugin": plugin, "deactivate": deactivate})


async def delete_plugin(plugin: str, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("delete-plugin", {"plugin": plugin})
