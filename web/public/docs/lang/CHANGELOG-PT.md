# Registro de alterações

Todas as alterações notáveis ​​no kit de ferramentas "Pixiv OAuth Token" serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto segue [Versão Semântica](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🔜 Em breve
- **Suporte Web Móvel** — O aplicativo Web atualmente oferece suporte apenas a navegadores de desktop. A próxima atualização trará suporte móvel totalmente responsivo, permitindo aos usuários gerar tokens Pixiv OAuth diretamente de dispositivos móveis sem precisar do aplicativo de desktop.

---

## [1.0.4] - 2026-03-29

### 🐞 Corrigido
- **CLI/GUI portátil — Reversão de versão após atualização**: `VERSION_FILE` e `CONFIG_FILE` foram resolvidos usando `Path(__file__)`, que no modo congelado (PyInstaller onefile) aponta para o diretório temporário `_MEIPASS` — um diretório que é destruído quando o aplicativo é fechado. Ambos os arquivos agora são resolvidos usando `_app_dir()` / `app_dir()` que retorna corretamente a pasta que contém o `.exe` real, garantindo que a identidade da versão persista durante as reinicializações.
- **CLI — A atualização substituiu temp `.py` em vez de exe**: Ao executar como um executável congelado, `_self_update()` estava substituindo o `.py` extraído dentro do diretório temporário em vez de substituir o `.exe` real. A função agora detecta `is_frozen` e baixa o novo executável diretamente, substituindo-o por um script atualizador `.bat` (mesmo mecanismo da GUI).

### ✨ Adicionado
- **Atualização automática com reconhecimento de arquitetura (CLI + GUI)**: os fluxos de atualização portáteis e de configuração agora detectam a arquitetura do executável em execução (`x64`, `x86`, `ARM64` ou genérico) a partir de seu nome de arquivo e baixam a variante de correspondência exata da pasta `downloads/`, evitando incompatibilidades acidentais de arquitetura durante as atualizações.
- **Fluxo de atualização do instalador de configuração CLI**: CLI agora espelha o comportamento da GUI para instalações de configuração — ao executar a partir de `Program Files`, ele baixa o instalador de configuração `.exe` mais recente e o executa silenciosamente (`/VERYSILENT /NORESTART`) em vez de tentar uma troca binária no local.

---
## [1.0.3] - 2026-03-26 
### ✨ Alterado
- Substituição do rótulo de compilação local padrão de `REL-LOCAL` para `BUILD-UNKNOWN` em ferramentas de tempo de execução/versão e manifestos gerados.
- A GUI agora inclui uma ação no menu superior **Changelog** e um menu suspenso **Versão** com entrada explícita de verificação de versão.
- Adicionada verificação automática de versão de inicialização na GUI com ações pop-up de atualização (**Atualizar** / **Mais tarde**), além de manipulação de fluxo de atualização para configuração congelada/distribuições portáteis.
- Geração de código de construção atualizada para `REL-U<unix_ms>` estilo unix em versões alteradas (`patch/minor/major`).

## [1.0.2] - 2026-03-23 
### ✨ Adicionado
- **Console de depuração (GUI)**
Um botão `⚙ Debug` dedicado no canto superior direito do cabeçalho da GUI abre um console de terminal com tema escuro que registra todos os eventos do aplicativo em tempo real. Os eventos capturados incluem: inicialização do aplicativo, alterações de idioma, todos os cliques de botão (login aberto, token do Exchange, token de atualização, token de acesso/atualização de cópia, tutorial), estados de solicitação HTTP (envio/sucesso/falha), etapas de fluxo PKCE, operações da área de transferência, gravações de configuração e avisos. Todas as mensagens de depuração estão totalmente localizadas em todos os 11 idiomas suportados. O console suporta transmissão ao vivo de novas mensagens enquanto abertas, pré-preenchimento de logs históricos desde o início da sessão, um botão **Copiar tudo** e um botão **Limpar**.

## [1.0.1] - 2026-03-22
### ✨ Adicionado
- **Limpador README inteligente para lançamentos**
Remove automaticamente seções de idioma de localização do arquivo `__p1__` ao compilar o `.zip` distribuível, substituindo links internos por links GitHub absolutos.
- **Suporte ao instalador duplo unificado**
O script do construtor InnoSetup agora gera um instalador unificado que solicita aos usuários finais que instalem opcionalmente a CLI independente ou a GUI gráfica.

### 🐞 Corrigido
- **Resolução do caminho de construção do instalador**
Corrigido um problema de incompatibilidade de caminho crítico em `make_installer_iss_dual.py`, onde `iscc` não conseguiu localizar `app\pixiv_oauth.ico` gerando arquivos de construção diretamente no diretório `scripts\` configurado.

## [1.0.0] - 2026-03-21
### ✨ Adicionado
- Distribuições executáveis ​​independentes iniciais (`.exe`) compiladas para modos GUI e CLI.
- Integração inicial otimizada sem servidor sincronizada com Vercel com detecção automática de idioma.
- Passagem de ofuscação extrema de JavaScript adicionada para endpoints da web.
