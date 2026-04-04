from automation_mcp.client import WordPressClient
from automation_mcp.media import optimize_image, image_to_base64
from pathlib import Path


async def upload_media(
    data: str = "",
    filename: str = "",
    alt_text: str = "",
    title: str = "",
    optimize: bool = False,
    format: str = "webp",
    max_width: int = 1200,
    quality: int = 85,
    path: str = "",
    site: str | None = None,
) -> dict:
    client = WordPressClient(site_name=site)

    # If local path provided, read and optionally optimize
    if path and Path(path).exists():
        if optimize:
            image_bytes, opt_filename = optimize_image(path, max_width=max_width, quality=quality, output_format=format)
            data = image_to_base64(image_bytes)
            filename = filename or opt_filename
        else:
            with open(path, "rb") as f:
                data = image_to_base64(f.read())
            filename = filename or Path(path).name

    params = {"data": data, "filename": filename}
    if alt_text: params["alt_text"] = alt_text
    if title: params["title"] = title

    return await client.execute("upload-media", params)


async def bulk_upload_media(
    items: list[dict],
    optimize: bool = False,
    format: str = "webp",
    max_width: int = 1200,
    quality: int = 85,
    site: str | None = None,
) -> dict:
    results = []
    for item in items:
        result = await upload_media(
            data=item.get("data", ""),
            filename=item.get("filename", ""),
            alt_text=item.get("alt_text", ""),
            title=item.get("title", ""),
            optimize=optimize,
            format=format,
            max_width=max_width,
            quality=quality,
            path=item.get("path", ""),
            site=site,
        )
        results.append(result.get("data", {}))

    return {"success": True, "data": {"uploads": results, "count": len(results)}}


async def list_media(site: str | None = None, **params) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("list-media", params)


async def delete_media(attachment_id: int, force: bool = False, site: str | None = None) -> dict:
    client = WordPressClient(site_name=site)
    return await client.execute("delete-media", {"attachment_id": attachment_id, "force": force})
