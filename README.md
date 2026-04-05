# Automation MCP

MCP server for full WordPress control via AI agents (Claude Code, Cursor, Claude Desktop).

## Architecture

```
AI Agent (Claude Code / Cursor / Claude Desktop)
    |
    v
MCP Server (Python - FastMCP)        <-- this repository
    |  HTTP POST
    v
WordPress Plugin (PHP - REST API)    <-- ~/automation-mcp-plugin/
    |
    v
WordPress (posts, pages, themes, plugins, media, DB, Elementor...)
```

## Requirements

- Python 3.10+
- WordPress with the **Automation MCP** plugin installed and active
- API key generated in the plugin panel (WP Admin > Automation MCP > API Keys)

## Installation

### 1. Install the MCP server

```bash
cd ~/automation-mcp
pipx install -e .
```

Or with pip:
```bash
pip install -e .
```

### 2. Register in Claude Code

```bash
claude mcp add automation-mcp -- automation-mcp
```

### 3. Install the WordPress plugin

1. Zip the `~/automation-mcp-plugin/` directory
2. In WP Admin, go to **Plugins > Add New > Upload Plugin**
3. Upload the ZIP and activate
4. Go to **Automation MCP > API Keys** and create a new key

### 4. Configure the site

Inside Claude Code (or another MCP client):

```
configure(action="add", name="mysite", url="https://mysite.com", api_key="amcp_xxxx...")
```

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
