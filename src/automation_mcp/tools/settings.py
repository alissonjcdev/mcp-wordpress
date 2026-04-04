from automation_mcp.client import WordPressClient


async def get_options(keys: list[str] | None = None, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    params = {}
    if keys: params["keys"] = keys
    return await client.execute("get-options", params)


async def update_options(options: dict, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("update-options", {"options": options})


async def manage_menus(site: str | None = None, **params) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("manage-menus", params)


async def manage_widgets(site: str | None = None, **params) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("manage-widgets", params)


async def manage_users(site: str | None = None, **params) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("manage-users", params)
