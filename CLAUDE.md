# Automation MCP

MCP server para controle total do WordPress via AI agents.

## Stack
- Python 3.10+ com MCP SDK (FastMCP)
- httpx para HTTP async
- Pillow para otimização de imagem

## Caminhos
- MCP Server: ~/automation-mcp/
- Plugin WordPress: ~/automation-mcp-plugin/
- Config: ~/.automation-mcp/config.json
- Entry point: automation-mcp (instalado via pipx)

## Elementor - Referência Essencial

### Cache (CRITICO)
Ao modificar `_elementor_data` via PHP, SEMPRE deletar:
```php
delete_post_meta($post_id, '_elementor_element_cache'); // HTML renderizado - O MAIS IMPORTANTE
delete_post_meta($post_id, '_elementor_css');
delete_post_meta($post_id, '_elementor_page_assets');
delete_option('_elementor_global_css');
delete_option('elementor_cache_time');
```

### Estrutura _elementor_data
JSON array de containers top-level. Cada elemento:
```json
{
  "id": "7chars",
  "elType": "container|widget",
  "widgetType": "text-editor|heading|image|html|social-icons|...",
  "settings": {},
  "elements": [],
  "isInner": true|false
}
```

### Dimensões
```json
{"unit": "px", "size": 40, "sizes": []}
```

### Spacing (padding/margin)
```json
{"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": false}
```

### Responsivo
Sufixo `_tablet` ou `_mobile` no nome do setting.

### Gotchas
- Widgets criados programaticamente (sem editor) NAO renderizam
- Para adicionar CSS/JS, usar widget HTML existente (criado via editor)
- `display: block !important` sobrescreve visibility responsiva - usar media queries
- `custom_css` usa "selector" como placeholder para `.elementor-element-{id}`
- Elementor 4.x pode não ter `.elementor-widget-container` wrapper

### Tool get-elementor-info
Use a tool `get_elementor_info` para descobrir automaticamente widgets disponíveis, breakpoints, cache keys, e estrutura de dados do Elementor instalado no site.
