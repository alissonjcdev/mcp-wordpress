# Automation MCP

MCP server para controle total do WordPress via AI agents (Claude Code, Cursor, Claude Desktop).

## Arquitetura

```
AI Agent (Claude Code / Cursor / Claude Desktop)
    |
    v
MCP Server (Python - FastMCP)        <-- este repositorio
    |  HTTP POST
    v
Plugin WordPress (PHP - REST API)    <-- ~/automation-mcp-plugin/
    |
    v
WordPress (posts, paginas, temas, plugins, media, DB, Elementor...)
```

## Requisitos

- Python 3.10+
- WordPress com o plugin **Automation MCP** instalado e ativo
- API key gerada no painel do plugin (WP Admin > Automation MCP > Chaves API)

## Instalacao

### 1. Instalar o MCP server

```bash
cd ~/automation-mcp
pipx install -e .
```

Ou com pip:
```bash
pip install -e .
```

### 2. Registrar no Claude Code

```bash
claude mcp add automation-mcp -- automation-mcp
```

### 3. Instalar o plugin WordPress

1. Comprimir o diretorio `~/automation-mcp-plugin/` como ZIP
2. No WP Admin, ir em **Plugins > Adicionar novo > Enviar plugin**
3. Fazer upload do ZIP e ativar
4. Ir em **Automation MCP > Chaves API** e criar uma nova chave

### 4. Configurar o site

Dentro do Claude Code (ou outro MCP client):

```
configure(action="add", name="meusite", url="https://meusite.com", api_key="amcp_xxxx...")
```

## Tools (39)

### Configure (1)
| Tool | Descricao |
|------|-----------|
| `configure` | Gerenciar sites: add, remove, list, test |

### Content Management (8)
| Tool | Descricao |
|------|-----------|
| `create_post` | Criar post, pagina ou CPT |
| `update_post` | Atualizar post existente |
| `delete_post` | Enviar post para lixeira ou deletar permanente |
| `list_posts` | Listar posts com filtros (tipo, status, busca, categoria) |
| `get_post` | Obter post completo por ID (conteudo, meta, categorias, imagem) |
| `manage_taxonomies` | Criar/listar/deletar categorias e tags |
| `manage_seo` | Gerenciar meta SEO (title, description, robots) |
| `manage_post_meta` | CRUD de post meta customizado |

### Themes (4)
| Tool | Descricao |
|------|-----------|
| `list_themes` | Listar temas instalados |
| `install_theme` | Instalar tema do repositorio WordPress |
| `activate_theme` | Ativar tema |
| `customize_theme` | Modificar opcoes do Customizer |

### Plugins (4)
| Tool | Descricao |
|------|-----------|
| `list_plugins` | Listar plugins instalados |
| `install_plugin` | Instalar plugin do repositorio WordPress |
| `activate_plugin` | Ativar/desativar plugin |
| `delete_plugin` | Deletar plugin |

### Media (3)
| Tool | Descricao |
|------|-----------|
| `upload_media` | Upload de arquivo para biblioteca de midia |
| `bulk_upload_media` | Upload em massa de multiplos arquivos |
| `list_media` | Listar itens da biblioteca de midia |
| `delete_media` | Deletar item de midia |

### Settings (5)
| Tool | Descricao |
|------|-----------|
| `get_options` | Ler opcoes do WordPress (site_url, blogname, etc) |
| `update_options` | Atualizar opcoes |
| `manage_menus` | Criar/editar menus de navegacao |
| `manage_widgets` | Gerenciar widgets e sidebars |
| `manage_users` | CRUD de usuarios WordPress |

### Low-Level (8)
| Tool | Descricao |
|------|-----------|
| `execute_php` | Executar codigo PHP arbitrario no WordPress |
| `wp_cli` | Executar comandos WP-CLI |
| `read_file` | Ler arquivo do servidor |
| `write_file` | Escrever arquivo no servidor |
| `edit_file` | Substituicao de texto em arquivo |
| `delete_file` | Deletar arquivo |
| `list_directory` | Listar conteudo de diretorio |
| `query_db` | Executar query SQL no banco de dados |

### Elementor (1)
| Tool | Descricao |
|------|-----------|
| `get_elementor_info` | Info completa: widgets, breakpoints, cache keys, estrutura de dados, gotchas |

### Diagnostics (4)
| Tool | Descricao |
|------|-----------|
| `get_site_overview` | Visao geral do site (versoes, plugins, tema, DB) |
| `site_health` | Diagnostico de saude do site |
| `clear_cache` | Limpar caches (Elementor, LiteSpeed, transients) |
| `optimize_db` | Otimizar tabelas do banco de dados |

## Elementor — Regras Obrigatorias

### Cache (CRITICO)
Ao modificar `_elementor_data` via `execute_php`, SEMPRE limpar caches:
```php
delete_post_meta($post_id, '_elementor_element_cache');
delete_post_meta($post_id, '_elementor_css');
delete_post_meta($post_id, '_elementor_page_assets');
delete_option('_elementor_global_css');
delete_option('elementor_cache_time');
```

### CSS Classes
Ao usar `custom_css` em um container/widget, SEMPRE adicionar `css_classes` com classe unica (ex: `rn-step-card`) para isolar escopo e evitar conflitos.

### Fidelidade Figma
Ao traduzir Figma para Elementor, validar fielmente: padding, gap, flex_direction, flex_align_items, flex_justify_content, width, min_height, border_radius, typography e cores. Usar metadata do Figma para derivar valores exatos.

## Seguranca

- Toda comunicacao usa HTTPS
- API keys com hash SHA-256 no banco
- Permissoes granulares por key (cada key tem abilities especificas)
- Rate limiting (100 req/min por key)
- Audit logging de todas as acoes
- User impersonation (acoes executam como usuario WP vinculado a key)

## Desenvolvimento

```bash
cd ~/automation-mcp
pip install -e ".[dev]"
pytest
```

## Licenca

Uso privado.
