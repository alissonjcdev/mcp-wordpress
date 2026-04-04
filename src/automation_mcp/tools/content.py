from automation_mcp.client import WordPressClient


async def create_post(site: str | None = None, **params) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("create-post", params)


async def update_post(site: str | None = None, **params) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("update-post", params)


async def delete_post(post_id: int, force: bool = False, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("delete-post", {"post_id": post_id, "force": force})


async def list_posts(site: str | None = None, **params) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("list-posts", params)


async def get_post(post_id: int, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("get-post", {"post_id": post_id})


async def manage_taxonomies(site: str | None = None, **params) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("manage-taxonomies", params)


async def manage_seo(site: str | None = None, **params) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("manage-seo", params)


async def manage_post_meta(site: str | None = None, **params) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("manage-post-meta", params)
