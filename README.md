# Automation MCP

MCP server for full WordPress control via AI agents (Claude Code, Cursor, Claude Desktop).

## What can it do?

- **Build entire Elementor pages** from Figma designs — containers, widgets, typography, colors, spacing
- **Create hover effects and animations** via custom CSS on Elementor containers
- **Manage multiple WordPress sites** from a single installation
- **Full content management** — create, edit, delete posts, pages and custom post types
- **Install themes and plugins** from the WordPress repository
- **Upload media** — images, SVGs, files with automatic optimization
- **Direct database access** — SQL queries, PHP execution, file management
- **SEO management** — meta titles, descriptions, robots directives
- **Elementor integration** — read structure, clear caches, get widget info
- **Site diagnostics** — health checks, cache clearing, database optimization

## Architecture

```
AI Agent (Claude Code / Cursor / Claude Desktop)
    |
    v
MCP Server (Python - FastMCP)        <-- this repository
    |  HTTP POST
    v
WordPress Plugin (PHP - REST API)    <-- included as ZIP in this repo
    |
    v
WordPress (posts, pages, themes, plugins, media, DB, Elementor...)
```

## Quick Start

### 1. Install the MCP server

```bash
pipx install git+https://github.com/alissonjcdev/mcp-wordpress.git
```

### 2. Register in Claude Code

```bash
claude mcp add automation-mcp -- automation-mcp
```

### 3. Install the WordPress plugin

1. Download [`automation-mcp-plugin.zip`](https://github.com/alissonjcdev/mcp-wordpress/releases/download/v1.0.0/automation-mcp-plugin.zip)
2. In WP Admin, go to **Plugins > Add New > Upload Plugin**
3. Upload the ZIP and activate
4. Go to **Automation MCP > API Keys** and create a new key

### 4. Configure the site

Inside Claude Code, use the `configure` tool:

```
configure(action="add", name="mysite", url="https://mysite.com", api_key="amcp_xxxx...")
```

Done. All 39 tools are now available.

## Multi-Site Management

You can add as many WordPress sites as you need:

```
configure(action="add", name="blog", url="https://blog.example.com", api_key="amcp_aaa...")
configure(action="add", name="store", url="https://store.example.com", api_key="amcp_bbb...")
configure(action="add", name="client-site", url="https://client.com", api_key="amcp_ccc...")
```

The first site added becomes the default. To target a specific site, use the `site` parameter on any tool:

```
list_posts(site="store")
create_post(title="New Product", type="post", site="client-site")
execute_php(code="phpinfo();", site="blog")
```

List all configured sites:
```
configure(action="list")
```

## Alternative Installation

<details>
<summary>With uvx (if you have uv installed)</summary>

```bash
claude mcp add automation-mcp -- uvx --from git+https://github.com/alissonjcdev/mcp-wordpress.git automation-mcp
```

Single command, no persistent install. Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).
</details>

<details>
<summary>From source (for development)</summary>

```bash
git clone https://github.com/alissonjcdev/mcp-wordpress.git
cd mcp-wordpress
pip install -e ".[dev]"
claude mcp add automation-mcp -- automation-mcp
```
</details>

## Requirements

- Python 3.10+
- [pipx](https://pipx.pypa.io/stable/installation/) (recommended) or pip
- WordPress with the **Automation MCP** plugin installed and active

## Tools (39)

### Configure (1)
| Tool | Description |
|------|-------------|
| `configure` | Manage sites: add, remove, list, test |

### Content Management (8)
| Tool | Description |
|------|-------------|
| `create_post` | Create post, page or CPT |
| `update_post` | Update existing post |
| `delete_post` | Trash or permanently delete post |
| `list_posts` | List posts with filters (type, status, search, category) |
| `get_post` | Get full post by ID (content, meta, categories, image) |
| `manage_taxonomies` | Create/list/delete categories and tags |
| `manage_seo` | Manage SEO meta (title, description, robots) |
| `manage_post_meta` | CRUD for custom post meta |

### Themes (4)
| Tool | Description |
|------|-------------|
| `list_themes` | List installed themes |
| `install_theme` | Install theme from WordPress repository |
| `activate_theme` | Activate theme |
| `customize_theme` | Modify Customizer options |

### Plugins (4)
| Tool | Description |
|------|-------------|
| `list_plugins` | List installed plugins |
| `install_plugin` | Install plugin from WordPress repository |
| `activate_plugin` | Activate/deactivate plugin |
| `delete_plugin` | Delete plugin |

### Media (4)
| Tool | Description |
|------|-------------|
| `upload_media` | Upload file to media library |
| `bulk_upload_media` | Bulk upload multiple files |
| `list_media` | List media library items |
| `delete_media` | Delete media item |

### Settings (5)
| Tool | Description |
|------|-------------|
| `get_options` | Read WordPress options (site_url, blogname, etc) |
| `update_options` | Update options |
| `manage_menus` | Create/edit navigation menus |
| `manage_widgets` | Manage widgets and sidebars |
| `manage_users` | CRUD for WordPress users |

### Low-Level (8)
| Tool | Description |
|------|-------------|
| `execute_php` | Execute arbitrary PHP code in WordPress |
| `wp_cli` | Run WP-CLI commands |
| `read_file` | Read file from server |
| `write_file` | Write file to server |
| `edit_file` | Text replacement in file |
| `delete_file` | Delete file |
| `list_directory` | List directory contents |
| `query_db` | Execute SQL query on database |

### Elementor (1)
| Tool | Description |
|------|-------------|
| `get_elementor_info` | Full info: widgets, breakpoints, cache keys, data structure, gotchas |

### Diagnostics (4)
| Tool | Description |
|------|-------------|
| `get_site_overview` | Site overview (versions, plugins, theme, DB) |
| `site_health` | Site health diagnostics |
| `clear_cache` | Clear caches (Elementor, LiteSpeed, transients) |
| `optimize_db` | Optimize database tables |

## Elementor — Mandatory Rules

### Cache (CRITICAL)
When modifying `_elementor_data` via `execute_php`, ALWAYS clear caches:
```php
delete_post_meta($post_id, '_elementor_element_cache');
delete_post_meta($post_id, '_elementor_css');
delete_post_meta($post_id, '_elementor_page_assets');
delete_option('_elementor_global_css');
delete_option('elementor_cache_time');
```

### CSS Classes
When using `custom_css` on a container/widget, ALWAYS add `css_classes` with a unique class (e.g. `rn-step-card`) to isolate scope and avoid conflicts.

### Figma Fidelity
When translating Figma to Elementor, faithfully validate: padding, gap, flex_direction, flex_align_items, flex_justify_content, width, min_height, border_radius, typography and colors. Use Figma metadata to derive exact values.

### Saving `_elementor_data` (CRITICAL)
Always use `wp_slash()` when saving Elementor data via `update_post_meta`. Without it, WordPress strips backslashes from the JSON string, corrupting the data structure:
```php
$json = json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
update_post_meta($post_id, '_elementor_data', wp_slash($json));
```

### HTML Attributes in Widget Content
When modifying the `editor` field of a `text-editor` widget programmatically, be aware that HTML attributes with quoted values (e.g. `<a href="...">`) can get corrupted by the encoding chain (`json_encode` → `wp_slash` → `update_post_meta`). Double-escaped quotes break links and other attributes in the rendered output.

Before inserting HTML with links or attributes, study how the widget stores that content natively via the Elementor editor UI. Each widget has its own way of handling rich content — always replicate the native format rather than assuming raw HTML will survive the encoding pipeline.

## Figma Best Practices

Organize your Figma design following these guidelines to get the best results when the agent translates it to your site.

### Structure

**Use Auto Layout on frames** — Auto Layout defines direction, spacing, and padding in a way the agent reads directly. A frame with Auto Layout becomes a well-structured block on your site with exact spacing preserved.

**Organize frame hierarchy** — Think of each frame as a block on your site. A parent frame containing child frames translates to a main container with inner blocks. The cleaner your layer tree, the more accurate the result.

**Name layers descriptively** — Names like "Hero Section", "Pricing Card", or "Footer Contact" make it easier to communicate with the agent about specific parts of your design. Instead of "Frame 47", use names that describe what the element is.

### Content

**Keep text as text layers** — Every text layer in Figma becomes an editable text block on your site. The agent extracts font family, size, weight, line height, and color automatically.

**Use high-quality images** — Place images in their final aspect ratio and size. The agent automatically optimizes them before uploading (converts to WebP, max 200KB, resized to 800px width).

**Keep icons as SVG components** — Vector icons stay sharp at any size on the site. Group your icons as components in Figma for easy reuse.

### Styles

**Use styles or variables for colors and typography** — When you define colors and text styles in Figma's design system (local styles or variables), the agent can extract consistent values across the entire design.

### Responsive

**Include mobile/tablet variations** — If your Figma file has frames for different screen sizes, the agent can apply specific breakpoints so the site adapts correctly on each device.

### Quick Reference: Figma → Site

| Figma Element | Site Result |
|---|---|
| Frame with Auto Layout | Structural block/container |
| Text layer | Editable text block |
| Rectangle/frame with image fill | Image |
| Icon/SVG component | Vector icon |
| Frame with text + icon | Icon box with text |
| Button (frame with text + background) | Clickable button |
| Group of social icons | Social media icon links |
| Frame with multiple cards | Item grid/list |
| Frame with background image + overlay | Hero section with background |
| Nested frames | Nested containers |

## Security

- All communication over HTTPS
- API keys hashed with SHA-256
- Granular per-key permissions (each key has specific abilities)
- Rate limiting (100 req/min per key)
- Audit logging of all actions
- User impersonation (actions execute as the WP user linked to the key)

## Development

```bash
cd ~/automation-mcp
pip install -e ".[dev]"
pytest
```

## License

Private use.
