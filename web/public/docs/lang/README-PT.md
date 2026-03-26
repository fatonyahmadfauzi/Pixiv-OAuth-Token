# Pixiv OAuth Token


> 🌐 Disponível em outros idiomas: [English](../../README.md) | [Polski](README-PL.md) | [中文](README-ZH.md) | [日本語](README-JP.md) | [Deutsch](README-DE.md) | [Français](README-FR.md) | [Español](README-ES.md) | [Русский](README-RU.md) | [Bahasa Indonesia](README-ID.md) | [한국어](README-KR.md)

---
Um kit de ferramentas para gerar tokens Pixiv OAuth em três modos:

- CLI (`app/pixiv_login.py`)
- GUI (`app/pixiv_login_gui.py`)
- Aplicativo Web (`web/public/` + API sem servidor)

## Requisitos

- Python 3.11+
- Windows (necessário para scripts de construção `.bat` e instalador Inno Setup)
- Dependências Python de `app/requirements.txt`

## Executar a partir da fonte

```bash
cd app
python -m pip install -r requirements.txt
python pixiv_login.py
```

Execute a GUI:

```bash
cd app
python pixiv_login_gui.py
```

### Recursos da GUI

| Recurso | Descrição |
|---|---|
| **Multilíngue** | 11 idiomas – detectados automaticamente na configuração, alternáveis ​​ao vivo via menu suspenso |
| **⚙ Console de depuração** | Botão no cabeçalho superior direito; abre um terminal escuro registrando **todos** eventos (cliques em botões, alterações de idioma, solicitações HTTP, etapas PKCE, área de transferência, configurações salvas, avisos) em tempo real e no idioma atual |
| **Troca de Tokens** | Cole URL pixiv:// ou código bruto → troca por acesso + token de atualização |
| **Token de atualização** | Atualização com um clique usando update_token salvo da configuração |
| **Copiar Tokens** | Copie access_token/refresh_token para a área de transferência instantaneamente |
| **Tutorial** | Guia de imagem passo a passo integrado ao aplicativo |

## Construir

### Construa todos os artefatos (CLI + GUI + Instalador + ZIP)

```bat
cd scripts
build_all_pro.bat patch
```

Argumento de versão:

- `patch`
- `minor`
- `major`
- `none`

Sinalizadores opcionais:

- `noinst` (pular instalador)
- `nosign` (pular assinatura)
- `nozip` (pular zip)
- `nogui` (pular GUI)
- `nopause` (sem pausa no final)

Exemplo:

```bat
cd scripts
build_all_pro.bat patch noinst nosign
```

### Principais saídas

- CLI portátil: `dist_portable\Pixiv OAuth CLi (Portable).exe`
- GUI portátil: `dist_gui\Pixiv OAuth GUi (Portable).exe`
- Instalador unificado: `dist_installer\PixivLoginSetup_v<version>.exe` (instala CLI + GUI)
- CLI do instalador: `dist_installer\Pixiv OAuth CLi Setup_v<version>.exe` (cópia do instalador unificado)
- GUI do instalador: `dist_installer\Pixiv OAuth GUi Setup_v<version>.exe` (cópia do instalador unificado)
- Liberar ZIP: `PixivOAuthRelease_v<version>.zip`
- Pasta sincronizada automaticamente: `downloads/` (último portátil/configuração + versão ZIP)

## Assinatura

Editar `scripts/sign_auto.bat`:

- `PFX_PATH`
- `PFX_PASS`
- `TS_URL`

Se o arquivo PFX estiver faltando, a assinatura será ignorada.

## Versionamento

A identidade da versão/construção do aplicativo é armazenada em `version.json`.

- `version`: versão semântica (`X.Y.Z`)
- `build_code`: identificador de compilação exclusivo

O substituto padrão de não lançamento agora é `BUILD-UNKNOWN` (em vez de `REL-LOCAL`), enquanto os lançamentos geram códigos de construção no estilo unix via `scripts/bump_version.py`:

- `REL-U<unix_ms>`

## Versão web (Vercel)

Um aplicativo da web altamente otimizado e responsivo com suporte dinâmico a vários idiomas (11 idiomas com detecção automática) e metadados de SEO abrangentes.

### Principais recursos da web
- **Páginas extensas**: página inicial, downloads, tutorial, contato, problemas e relações públicas, rastreador de discussões, visualizador de documentação Markdown e integração de suporte/doações.
- **SEO avançado**: tags `<meta>` localizadas injetadas automaticamente, dados estruturados JSON-LD extensos (Sitelinks, SoftwareApplication, etc.), geração automatizada de `hreflang`, `robots.txt` e `sitemap.xml`.
- **Segurança e desempenho**: ofuscação automática de JavaScript (manipulação extrema), minificação de HTML/CSS (via `cd web && node build_minify.js`) e prevenção limpa de `XSS` via `escapeHTML`.
- **GitHub API Proxy**: solicitações de proxy GitHub API de endpoints Vercel sem servidor (`/api/github`) usando um token de acesso pessoal (`GITHUB_PAT`) para ignorar completamente os limites de taxa pública.

### Implantar no Vercel

1. Envie o repositório para GitHub.
2. Vercel → **Adicionar Novo...** → **Projeto** → importe este repositório.
3. Defina suas variáveis ​​de ambiente no Vercel:
- `PIXIV_CLIENT_SECRET`: Seu segredo do cliente Pixiv OAuth.
- `GITHUB_PAT`: opcional, mas altamente recomendado (seu token de acesso pessoal GitHub para evitar limites de taxa em emissões e lançamentos de recompra).
4. `vercel.json` já configura:
- URLs limpos (remoção de `.html`)
- Hospedagem estática de `public/`
- APIs sem servidor em `/api/*`
- Roteamento de página 404 personalizado integrado
- Cache de futuro distante por meio de cabeçalhos Edge Cache.
5. Implante.

> [!IMPORTANTE]
> Se você fizer alterações em HTML, CSS ou JS, lembre-se de executar `cd web && node build_minify.js` antes de implantar para ofuscar automaticamente o código e compactar ativos.

> Nota de segurança: para produção, sempre defina `PIXIV_CLIENT_SECRET` nas variáveis ​​de ambiente do seu projeto Vercel.

## Baixe o aplicativo (versão mais recente)

URL base:

`https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download`

Arquivos:

- GUI portátil: `Pixiv OAuth GUi (Portable).exe`
- GUI de configuração: `Pixiv OAuth GUi Setup_v<version>.exe`
- CLI portátil: `Pixiv OAuth CLi (Portable).exe`
- CLI de configuração: `Pixiv OAuth CLi Setup_v<version>.exe`

### PowerShell (detecta automaticamente os ativos da versão mais recente)

```powershell
$api = "https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest"
$assets = (Invoke-RestMethod -Uri $api).assets

function Get-AssetUrl([string]$pattern) {
  ($assets | Where-Object { $_.name -match $pattern } | Select-Object -First 1).browser_download_url
}

$guiPortable = Get-AssetUrl "Pixiv OAuth GUi \(Portable\)"
$cliPortable = Get-AssetUrl "Pixiv OAuth CLi \(Portable\)"
$guiSetup    = Get-AssetUrl "Pixiv OAuth GUi Setup"
$cliSetup    = Get-AssetUrl "Pixiv OAuth CLi Setup"

Invoke-WebRequest $guiPortable -OutFile "Pixiv OAuth GUi (Portable).exe"
Invoke-WebRequest $cliPortable -OutFile "Pixiv OAuth CLi (Portable).exe"
Invoke-WebRequest $guiSetup    -OutFile "Pixiv OAuth GUi Setup.exe"
Invoke-WebRequest $cliSetup    -OutFile "Pixiv OAuth CLi Setup.exe"
```

### PowerShell (URLs fixos de `downloads/`)

```powershell
$guiPortable = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/raw/HEAD/downloads/Pixiv%20OAuth%20GUi%20(Portable)_latest.exe"
$cliPortable = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/raw/HEAD/downloads/Pixiv%20OAuth%20CLi%20(Portable)_latest.exe"
$guiSetup    = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/raw/HEAD/downloads/Pixiv%20OAuth%20GUi%20Setup_latest.exe"
$cliSetup    = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/raw/HEAD/downloads/Pixiv%20OAuth%20CLi%20Setup_latest.exe"

Invoke-WebRequest $guiPortable -OutFile "Pixiv OAuth GUi (Portable).exe"
Invoke-WebRequest $cliPortable -OutFile "Pixiv OAuth CLi (Portable).exe"
Invoke-WebRequest $guiSetup    -OutFile "Pixiv OAuth GUi Setup.exe"
Invoke-WebRequest $cliSetup    -OutFile "Pixiv OAuth CLi Setup.exe"
```

Execute isso no **PowerShell** (não no CMD).

Se você apenas executar:

```powershell
$guiPortable = "..."
```

e nada aparece, isso é esperado. Ele armazena apenas um valor em uma variável. O download começa quando você executa `Invoke-WebRequest`.

Depois que o download terminar e o PowerShell retornar para `PS C:\...>` sem erro:

```powershell
Get-ChildItem "Pixiv OAuth GUi (Portable).exe"
Start-Process ".\Pixiv OAuth GUi (Portable).exe"
```

Para compilação do instalador:

```powershell
Invoke-WebRequest $guiSetup -OutFile "Pixiv OAuth GUi Setup.exe"
Start-Process ".\Pixiv OAuth GUi Setup.exe"
```

Se a política TLS bloquear o download:

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

### CMD (detecta automaticamente os ativos de lançamento mais recentes)

```cmd
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi Setup.exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi Setup.exe"
```

## Instalação do Python

```bash
cd app
python -m pip install -r requirements.txt
```

Ou instale diretamente de GitHub:

```bash
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"
```

## 🧾 Registro de alterações

Veja todas as alterações notáveis ​​para cada versão no arquivo [Registro de alterações](CHANGELOG-PT.md).
📦 Você também pode visualizar as notas de lançamento diretamente na [página de lançamentos GitHub](https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases).

## Licença

MIT License. Consulte `LICENSE`.
