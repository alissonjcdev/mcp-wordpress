import json

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("automation-mcp")


# ─── Configure ───


@mcp.tool()
async def configure(
    action: str = "list",
    name: str | None = None,
    url: str | None = None,
    api_key: str | None = None,
    label: str | None = None,
    set_default: bool = False,
) -> str:
    """View or update Automation MCP site configuration.

    Args:
        action: Operation: "list", "add", "remove", "test". Default: list
        name: Site identifier name (used in other tools as 'site' param).
        url: WordPress site URL (e.g. https://mysite.com).
        api_key: API key generated in the Automation MCP plugin.
        label: Human-readable label for the site.
        set_default: Set this site as default after adding.
    """
    from automation_mcp.config import load_config, save_config
    from automation_mcp.client import WordPressClient

    config = load_config()

    if action == "list":
        display = dict(config)
        for sn, sd in display.get("sites", {}).items():
            if sd.get("api_key"):
                sd["api_key"] = sd["api_key"][:12] + "..." + sd["api_key"][-4:]
        return json.dumps(display, ensure_ascii=False, indent=2)

    if action == "add":
        if not name or not url or not api_key:
            return json.dumps({"error": "Campos 'name', 'url' e 'api_key' são obrigatórios."}, ensure_ascii=False)
        config.setdefault("sites", {})[name] = {"url": url.rstrip("/"), "api_key": api_key, "label": label or name}
        if set_default or not config.get("default_site"):
            config["default_site"] = name
        save_config(config)
        return json.dumps({"success": True, "message": f"Site '{name}' adicionado."}, ensure_ascii=False, indent=2)

    if action == "remove":
        if not name or name not in config.get("sites", {}):
            return json.dumps({"error": f"Site '{name}' não encontrado."}, ensure_ascii=False)
        del config["sites"][name]
        if config.get("default_site") == name:
            config["default_site"] = next(iter(config["sites"]), "")
        save_config(config)
        return json.dumps({"success": True, "message": f"Site '{name}' removido."}, ensure_ascii=False, indent=2)

    if action == "test":
        try:
            client = WordPressClient(site_name=name)
            result = await client.ping()
            return json.dumps({"success": True, "connection": result.get("data", {})}, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False, indent=2)

    return json.dumps({"error": f"Ação '{action}' inválida."}, ensure_ascii=False)


# ─── Content Management ───


@mcp.tool()
async def create_post(
    title: str,
    content: str = "",
    status: str = "draft",
    type: str = "post",
    excerpt: str = "",
    categories: list[int] | None = None,
    tags: list[str] | None = None,
    featured_image: int | None = None,
    slug: str = "",
    author: int | None = None,
    site: str | None = None,
) -> str:
    """Create a new WordPress post or page.

    Args:
        title: Post title.
        content: Post content (HTML).
        status: Post status: draft, publish, pending, private. Default: draft
        type: Post type: post, page, or any registered CPT. Default: post
        excerpt: Post excerpt/summary.
        categories: List of category IDs.
        tags: List of tag names.
        featured_image: Attachment ID for featured image.
        slug: URL slug.
        author: Author user ID.
        site: Target site name from config. Uses default if omitted.
    """
    from automation_mcp.tools.content import create_post as _fn
    params = {"title": title, "content": content, "status": status, "type": type}
    if excerpt: params["excerpt"] = excerpt
    if categories: params["categories"] = categories
    if tags: params["tags"] = tags
    if featured_image: params["featured_image"] = featured_image
    if slug: params["slug"] = slug
    if author: params["author"] = author
    result = await _fn(site=site, **params)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def update_post(
    post_id: int,
    title: str | None = None,
    content: str | None = None,
    status: str | None = None,
    excerpt: str | None = None,
    categories: list[int] | None = None,
    tags: list[str] | None = None,
    featured_image: int | None = None,
    slug: str | None = None,
    site: str | None = None,
) -> str:
    """Update an existing WordPress post or page.

    Args:
        post_id: ID of the post to update.
        title: New title.
        content: New content (HTML).
        status: New status.
        excerpt: New excerpt.
        categories: New category IDs.
        tags: New tags.
        featured_image: New featured image attachment ID.
        slug: New URL slug.
        site: Target site name from config.
    """
    from automation_mcp.tools.content import update_post as _fn
    params = {"post_id": post_id}
    if title is not None: params["title"] = title
    if content is not None: params["content"] = content
    if status is not None: params["status"] = status
    if excerpt is not None: params["excerpt"] = excerpt
    if categories is not None: params["categories"] = categories
    if tags is not None: params["tags"] = tags
    if featured_image is not None: params["featured_image"] = featured_image
    if slug is not None: params["slug"] = slug
    result = await _fn(site=site, **params)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def delete_post(post_id: int, force: bool = False, site: str | None = None) -> str:
    """Delete a WordPress post or page.

    Args:
        post_id: ID of the post to delete.
        force: If true, permanently delete. If false, move to trash. Default: false
        site: Target site name from config.
    """
    from automation_mcp.tools.content import delete_post as _fn
    result = await _fn(post_id=post_id, force=force, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def list_posts(
    type: str = "post",
    status: str = "any",
    per_page: int = 20,
    page: int = 1,
    search: str = "",
    category: int | None = None,
    author: int | None = None,
    orderby: str = "date",
    order: str = "DESC",
    site: str | None = None,
) -> str:
    """List WordPress posts with filters.

    Args:
        type: Post type: post, page, or CPT name. Default: post
        status: Filter by status: any, publish, draft, pending, trash. Default: any
        per_page: Results per page (max 100). Default: 20
        page: Page number. Default: 1
        search: Search term.
        category: Filter by category ID.
        author: Filter by author user ID.
        orderby: Sort by: date, title, modified, rand. Default: date
        order: Sort order: ASC or DESC. Default: DESC
        site: Target site name from config.
    """
    from automation_mcp.tools.content import list_posts as _fn
    params = {"type": type, "status": status, "per_page": per_page, "page": page, "orderby": orderby, "order": order}
    if search: params["search"] = search
    if category: params["category"] = category
    if author: params["author"] = author
    result = await _fn(site=site, **params)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def get_post(post_id: int, site: str | None = None) -> str:
    """Get a complete WordPress post by ID, including content, meta, categories, tags, and featured image.

    Args:
        post_id: ID of the post.
        site: Target site name from config.
    """
    from automation_mcp.tools.content import get_post as _fn
    result = await _fn(post_id=post_id, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def manage_taxonomies(
    operation: str = "list",
    taxonomy: str = "category",
    name: str = "",
    description: str = "",
    slug: str = "",
    parent: int = 0,
    term_id: int | None = None,
    site: str | None = None,
) -> str:
    """Manage WordPress taxonomies (categories, tags, custom taxonomies).

    Args:
        operation: Operation: list, create, update, delete. Default: list
        taxonomy: Taxonomy name: category, post_tag, or custom. Default: category
        name: Term name (for create/update).
        description: Term description.
        slug: Term slug.
        parent: Parent term ID (for hierarchical taxonomies).
        term_id: Term ID (for update/delete).
        site: Target site name from config.
    """
    from automation_mcp.tools.content import manage_taxonomies as _fn
    params = {"operation": operation, "taxonomy": taxonomy}
    if name: params["name"] = name
    if description: params["description"] = description
    if slug: params["slug"] = slug
    if parent: params["parent"] = parent
    if term_id: params["term_id"] = term_id
    result = await _fn(site=site, **params)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def manage_seo(
    post_id: int,
    operation: str = "get",
    title: str | None = None,
    description: str | None = None,
    focus_keyword: str | None = None,
    og_image: str | None = None,
    site: str | None = None,
) -> str:
    """Manage SEO meta fields for a post (compatible with Yoast SEO and RankMath).

    Args:
        post_id: ID of the post.
        operation: Operation: get or set. Default: get
        title: SEO title.
        description: Meta description.
        focus_keyword: Focus keyword.
        og_image: Open Graph image URL.
        site: Target site name from config.
    """
    from automation_mcp.tools.content import manage_seo as _fn
    params = {"post_id": post_id, "operation": operation}
    if title is not None: params["title"] = title
    if description is not None: params["description"] = description
    if focus_keyword is not None: params["focus_keyword"] = focus_keyword
    if og_image is not None: params["og_image"] = og_image
    result = await _fn(site=site, **params)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def manage_post_meta(
    post_id: int,
    operation: str = "get",
    key: str | None = None,
    value: str | None = None,
    site: str | None = None,
) -> str:
    """Manage custom meta fields for a post (ACF, JetEngine, Pods, etc).

    Args:
        post_id: ID of the post.
        operation: Operation: get, set, delete. Default: get
        key: Meta field key. If omitted on 'get', returns all meta.
        value: Meta field value (for 'set' operation).
        site: Target site name from config.
    """
    from automation_mcp.tools.content import manage_post_meta as _fn
    params = {"post_id": post_id, "operation": operation}
    if key is not None: params["key"] = key
    if value is not None: params["value"] = value
    result = await _fn(site=site, **params)
    return json.dumps(result, ensure_ascii=False, indent=2)


# ─── Themes ───


@mcp.tool()
async def list_themes(site: str | None = None) -> str:
    """List all installed WordPress themes with active status.

    Args:
        site: Target site name from config.
    """
    from automation_mcp.tools.themes import list_themes as _fn
    result = await _fn(site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def install_theme(slug: str, site: str | None = None) -> str:
    """Install a theme from the WordPress repository.

    Args:
        slug: Theme slug from wordpress.org (e.g. 'astra', 'flavflavor').
        site: Target site name from config.
    """
    from automation_mcp.tools.themes import install_theme as _fn
    result = await _fn(slug=slug, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def activate_theme(slug: str, site: str | None = None) -> str:
    """Activate an installed WordPress theme.

    Args:
        slug: Theme directory slug.
        site: Target site name from config.
    """
    from automation_mcp.tools.themes import activate_theme as _fn
    result = await _fn(slug=slug, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def customize_theme(settings: dict, site: str | None = None) -> str:
    """Modify theme customizer options (logo, colors, menus, header/footer).

    Args:
        settings: Dict of theme_mod key-value pairs to set.
        site: Target site name from config.
    """
    from automation_mcp.tools.themes import customize_theme as _fn
    result = await _fn(settings=settings, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


# ─── Plugins ───


@mcp.tool()
async def list_plugins(site: str | None = None) -> str:
    """List all installed WordPress plugins with activation status and available updates.

    Args:
        site: Target site name from config.
    """
    from automation_mcp.tools.plugins import list_plugins as _fn
    result = await _fn(site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def install_plugin(slug: str, site: str | None = None) -> str:
    """Install a plugin from the WordPress repository.

    Args:
        slug: Plugin slug from wordpress.org (e.g. 'yoast-seo', 'jetengine').
        site: Target site name from config.
    """
    from automation_mcp.tools.plugins import install_plugin as _fn
    result = await _fn(slug=slug, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def activate_plugin(plugin: str, deactivate: bool = False, site: str | None = None) -> str:
    """Activate or deactivate a WordPress plugin.

    Args:
        plugin: Plugin file path (e.g. 'jetengine/jet-engine.php').
        deactivate: If true, deactivate instead of activate. Default: false
        site: Target site name from config.
    """
    from automation_mcp.tools.plugins import activate_plugin as _fn
    result = await _fn(plugin=plugin, deactivate=deactivate, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def delete_plugin(plugin: str, site: str | None = None) -> str:
    """Delete a WordPress plugin (deactivates first if active).

    Args:
        plugin: Plugin file path (e.g. 'hello-dolly/hello.php').
        site: Target site name from config.
    """
    from automation_mcp.tools.plugins import delete_plugin as _fn
    result = await _fn(plugin=plugin, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


# ─── Media ───


@mcp.tool()
async def upload_media(
    path: str = "",
    data: str = "",
    filename: str = "",
    alt_text: str = "",
    title: str = "",
    optimize: bool = False,
    format: str = "webp",
    max_width: int = 1200,
    quality: int = 85,
    site: str | None = None,
) -> str:
    """Upload an image or file to the WordPress media library with optional optimization.

    Args:
        path: Local file path (for images generated by nano-banana or other tools).
        data: Base64-encoded file data or URL (alternative to path).
        filename: Output filename.
        alt_text: Image alt text for accessibility and SEO.
        title: Media title.
        optimize: Auto-optimize before upload (resize, compress, convert). Default: false
        format: Output format when optimizing: webp, jpeg, png. Default: webp
        max_width: Max width in pixels when optimizing. Default: 1200
        quality: Compression quality 1-100. Default: 85
        site: Target site name from config.
    """
    from automation_mcp.tools.media import upload_media as _fn
    result = await _fn(path=path, data=data, filename=filename, alt_text=alt_text, title=title, optimize=optimize, format=format, max_width=max_width, quality=quality, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def bulk_upload_media(
    items: list[dict],
    optimize: bool = False,
    format: str = "webp",
    max_width: int = 1200,
    quality: int = 85,
    site: str | None = None,
) -> str:
    """Upload multiple images to the WordPress media library at once.

    Args:
        items: List of dicts with keys: path (or data), filename, alt_text, title.
        optimize: Auto-optimize all images. Default: false
        format: Output format for optimization. Default: webp
        max_width: Max width for optimization. Default: 1200
        quality: Compression quality. Default: 85
        site: Target site name from config.
    """
    from automation_mcp.tools.media import bulk_upload_media as _fn
    result = await _fn(items=items, optimize=optimize, format=format, max_width=max_width, quality=quality, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def list_media(
    per_page: int = 20,
    page: int = 1,
    mime_type: str = "",
    search: str = "",
    site: str | None = None,
) -> str:
    """List media library items with filters.

    Args:
        per_page: Results per page (max 100). Default: 20
        page: Page number. Default: 1
        mime_type: Filter by MIME type (e.g. 'image/jpeg', 'image').
        search: Search term.
        site: Target site name from config.
    """
    from automation_mcp.tools.media import list_media as _fn
    params = {"per_page": per_page, "page": page}
    if mime_type: params["mime_type"] = mime_type
    if search: params["search"] = search
    result = await _fn(site=site, **params)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def delete_media(attachment_id: int, force: bool = False, site: str | None = None) -> str:
    """Delete a media item from the WordPress library.

    Args:
        attachment_id: ID of the attachment to delete.
        force: Permanently delete (true) or move to trash (false). Default: false
        site: Target site name from config.
    """
    from automation_mcp.tools.media import delete_media as _fn
    result = await _fn(attachment_id=attachment_id, force=force, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


# ─── Settings ───


@mcp.tool()
async def get_options(
    keys: list[str] | None = None,
    site: str | None = None,
) -> str:
    """Read WordPress site options/settings.

    Args:
        keys: List of option keys to read. Default: common options (blogname, siteurl, etc).
        site: Target site name from config.
    """
    from automation_mcp.tools.settings import get_options as _fn
    result = await _fn(keys=keys, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def update_options(options: dict, site: str | None = None) -> str:
    """Update WordPress site options/settings.

    Args:
        options: Dict of option key-value pairs to update.
        site: Target site name from config.
    """
    from automation_mcp.tools.settings import update_options as _fn
    result = await _fn(options=options, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def manage_menus(
    operation: str = "list",
    menu_id: int | None = None,
    name: str = "",
    title: str = "",
    url: str = "",
    item_type: str = "custom",
    object: str = "",
    object_id: int = 0,
    site: str | None = None,
) -> str:
    """Manage WordPress navigation menus and menu items.

    Args:
        operation: Operation: list, create, add_item, delete. Default: list
        menu_id: Menu ID (for add_item, delete).
        name: Menu name (for create).
        title: Menu item title (for add_item).
        url: Menu item URL (for add_item with custom type).
        item_type: Menu item type: custom, post_type, taxonomy. Default: custom
        object: Object type (for post_type/taxonomy items).
        object_id: Object ID (for post_type/taxonomy items).
        site: Target site name from config.
    """
    from automation_mcp.tools.settings import manage_menus as _fn
    params = {"operation": operation}
    if menu_id: params["menu_id"] = menu_id
    if name: params["name"] = name
    if title: params["title"] = title
    if url: params["url"] = url
    if item_type != "custom": params["item_type"] = item_type
    if object: params["object"] = object
    if object_id: params["object_id"] = object_id
    result = await _fn(site=site, **params)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def manage_widgets(
    operation: str = "list",
    site: str | None = None,
) -> str:
    """Manage WordPress widgets and sidebars.

    Args:
        operation: Operation: list. Default: list
        site: Target site name from config.
    """
    from automation_mcp.tools.settings import manage_widgets as _fn
    result = await _fn(site=site, operation=operation)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def manage_users(
    operation: str = "list",
    per_page: int = 20,
    role: str = "",
    login: str = "",
    email: str = "",
    password: str = "",
    display_name: str = "",
    user_id: int | None = None,
    reassign: int | None = None,
    site: str | None = None,
) -> str:
    """Manage WordPress users and roles.

    Args:
        operation: Operation: list, create, delete. Default: list
        per_page: Results per page (for list). Default: 20
        role: Filter/assign role (e.g. administrator, editor, subscriber).
        login: Username (for create).
        email: Email (for create).
        password: Password (for create, auto-generated if omitted).
        display_name: Display name (for create).
        user_id: User ID (for delete).
        reassign: Reassign posts to this user ID on delete.
        site: Target site name from config.
    """
    from automation_mcp.tools.settings import manage_users as _fn
    params = {"operation": operation}
    if operation == "list":
        params["per_page"] = per_page
        if role: params["role"] = role
    elif operation == "create":
        if login: params["login"] = login
        if email: params["email"] = email
        if password: params["password"] = password
        if role: params["role"] = role
        if display_name: params["display_name"] = display_name
    elif operation == "delete":
        if user_id: params["user_id"] = user_id
        if reassign: params["reassign"] = reassign
    result = await _fn(site=site, **params)
    return json.dumps(result, ensure_ascii=False, indent=2)


# ─── Low-Level ───


@mcp.tool()
async def execute_php(code: str, site: str | None = None) -> str:
    """Execute arbitrary PHP code with full access to the WordPress environment.

    Args:
        code: PHP code to execute (without <?php tags).
        site: Target site name from config.
    """
    from automation_mcp.tools.lowlevel import execute_php as _fn
    result = await _fn(code=code, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def wp_cli(command: str, site: str | None = None) -> str:
    """Execute a WP-CLI command on the WordPress server.

    Args:
        command: WP-CLI command (without 'wp' prefix, e.g. 'plugin list', 'post list --post_type=page').
        site: Target site name from config.
    """
    from automation_mcp.tools.lowlevel import wp_cli as _fn
    result = await _fn(command=command, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def read_file(path: str, site: str | None = None) -> str:
    """Read a file from the WordPress server. Binary files are returned as base64.

    Args:
        path: File path relative to WordPress root (e.g. 'wp-content/themes/mytheme/style.css').
        site: Target site name from config.
    """
    from automation_mcp.tools.lowlevel import read_file as _fn
    result = await _fn(path=path, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def write_file(path: str, content: str, site: str | None = None) -> str:
    """Create or overwrite a file on the WordPress server. Protected directories are blocked.

    Args:
        path: File path relative to WordPress root.
        content: File content to write.
        site: Target site name from config.
    """
    from automation_mcp.tools.lowlevel import write_file as _fn
    result = await _fn(path=path, content=content, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def edit_file(path: str, search: str, replace: str, site: str | None = None) -> str:
    """Apply a targeted text replacement to a file on the WordPress server.

    Args:
        path: File path relative to WordPress root.
        search: Text to find.
        replace: Text to replace with.
        site: Target site name from config.
    """
    from automation_mcp.tools.lowlevel import edit_file as _fn
    result = await _fn(path=path, search=search, replace=replace, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def delete_file(path: str, site: str | None = None) -> str:
    """Delete a file or directory on the WordPress server. Critical WordPress directories are protected.

    Args:
        path: File/directory path relative to WordPress root.
        site: Target site name from config.
    """
    from automation_mcp.tools.lowlevel import delete_file as _fn
    result = await _fn(path=path, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def list_directory(
    path: str = ".",
    recursive: bool = False,
    glob: str = "*",
    site: str | None = None,
) -> str:
    """List directory contents on the WordPress server with glob filtering.

    Args:
        path: Directory path relative to WordPress root. Default: root
        recursive: Recurse into subdirectories. Default: false
        glob: Glob pattern to filter files (e.g. '*.php', '*.css'). Default: *
        site: Target site name from config.
    """
    from automation_mcp.tools.lowlevel import list_directory as _fn
    result = await _fn(path=path, recursive=recursive, glob=glob, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def query_db(sql: str, site: str | None = None) -> str:
    """Execute a SQL query on the WordPress database. Supports SELECT, INSERT, UPDATE, DELETE.

    Args:
        sql: SQL query to execute.
        site: Target site name from config.
    """
    from automation_mcp.tools.lowlevel import query_db as _fn
    result = await _fn(sql=sql, site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


# ─── Diagnostics ───


@mcp.tool()
async def get_site_overview(site: str | None = None) -> str:
    """Get a complete overview of the WordPress site: version, theme, plugins, CPTs, taxonomies, users, DB size.

    Args:
        site: Target site name from config.
    """
    from automation_mcp.tools.diagnostics import get_site_overview as _fn
    result = await _fn(site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def site_health(site: str | None = None) -> str:
    """Run WordPress Site Health diagnostics and return test results.

    Args:
        site: Target site name from config.
    """
    from automation_mcp.tools.diagnostics import site_health as _fn
    result = await _fn(site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def clear_cache(site: str | None = None) -> str:
    """Clear all WordPress caches: transients, object cache, and page cache.

    Args:
        site: Target site name from config.
    """
    from automation_mcp.tools.diagnostics import clear_cache as _fn
    result = await _fn(site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def optimize_db(site: str | None = None) -> str:
    """Optimize the WordPress database: clean revisions, expired transients, spam, trash, and optimize tables.

    Args:
        site: Target site name from config.
    """
    from automation_mcp.tools.diagnostics import optimize_db as _fn
    result = await _fn(site=site)
    return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
