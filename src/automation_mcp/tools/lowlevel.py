from automation_mcp.client import WordPressClient


async def execute_php(code: str, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("execute-php", {"code": code})


async def wp_cli(command: str, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("wp-cli", {"command": command})


async def read_file(path: str, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("read-file", {"path": path})


async def write_file(path: str, content: str, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("write-file", {"path": path, "content": content})


async def edit_file(path: str, search: str, replace: str, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("edit-file", {"path": path, "search": search, "replace": replace})


async def delete_file(path: str, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("delete-file", {"path": path})


async def list_directory(path: str = ".", recursive: bool = False, glob: str = "*", site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("list-directory", {"path": path, "recursive": recursive, "glob": glob})


async def query_db(sql: str, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("query-db", {"sql": sql})
