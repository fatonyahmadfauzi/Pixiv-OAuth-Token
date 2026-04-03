# Registro de alterações

All notable changes to the "Pixiv OAuth Token" toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🔜 Coming Soon

- **Mobile Web Support** — The web app currently only supports desktop browsers. Upcoming update will bring full responsive mobile support, allowing users to generate Pixiv OAuth tokens directly from mobile devices without needing the desktop app.


---

## [1.0.5] - 2026-04-03

### ✨ Adicionado

- **Inicialização GUI com reconhecimento de Internet**
Antes de iniciar a janela principal GUI, uma tela inicial inteligente `NetLoadingScreen` agora executa uma verificação de conectividade com a Internet antes do voo. Se nenhuma conexão for encontrada, ele tentará novamente em segundo plano até se conectar. Além disso, um monitor de tempo de execução ativo exibirá um alerta voltando para a tela de carregamento se a conexão cair no meio do uso.
- **Modos de documentação GUI nativos**
Redirecionamentos de navegador externo substituídos para documentação crítica. **Registro de alterações**, **Termos e Condições** e **Política de Privacidade** agora são exibidos em janelas de diálogo `tkinter` nativas, dinâmicas e limpas (buscando de forma assíncrona diretamente do repositório GitHub).
- **Localizações abrangentes de terminais**
A interface interativa GitHub CLI (navegação de problemas) e todos os layouts jurídicos/de suporte baseados em terminal agora estão autenticamente localizados em todos os 11 idiomas suportados.

### ✨ Alterado

- **Estética CLI redesenhada**
Removidas as bordas decorativas da caixa legada para um display de terminal significativamente mais limpo, modernizado e alinhado à esquerda.
- **Assinatura de código digital automatizada**
Atualizou substancialmente o pipeline `sign_auto.bat`. O script agora descobre automaticamente `signtool.exe` profundamente no SDK do Windows, aplicando sem esforço o certificado autoassinado em todas as compilações geradas simultaneamente (incluindo configurações do instalador e aliases de download `_latest`) para suprimir sinalizadores básicos de 'Editor Desconhecido' do SmartScreen.

### 🐞 Corrigido

- **Bug nas propriedades do instalador**
Corrigida uma anomalia em que o instalador `Setup.exe` exibia `0.0.0.0` nas Propriedades do Windows. O construtor agora injeta corretamente os cabeçalhos PE `VersionInfoVersion` estritos durante a compilação para refletir o número de versão correspondente exato (e.g., 1.0.5.0) imediatamente após a renderização.

---

## [1.0.4] - 2026-03-29

### 🐞 Corrigido

- **Portátil CLI/GUI — Reversão de versão após atualização**: `VERSION_FILE` e `CONFIG_FILE` foram resolvidos usando `Path(__file__)`, que no modo congelado (PyInstaller onefile) aponta para o diretório temporário `_MEIPASS` — um diretório que é destruído quando o aplicativo é fechado. Ambos os arquivos agora são resolvidos usando `_app_dir()` / `app_dir()` que retorna corretamente a pasta que contém o `.exe` real, garantindo que a identidade da versão persista durante as reinicializações.
- **CLI — A atualização substituiu temp `.py` em vez de exe**: Ao executar como um executável congelado, `_self_update()` estava substituindo o `.py` extraído dentro do diretório temporário em vez de substituir o `.exe` real. A função agora detecta `is_frozen` e baixa o novo executável diretamente, substituindo-o por um script atualizador `.bat` (mesmo mecanismo do GUI).

### ✨ Adicionado

- **Atualização automática com reconhecimento de arquitetura (CLI + GUI)**: os fluxos de atualização portátil e de configuração agora detectam a arquitetura do executável em execução (`x64`, `x86`, `ARM64` ou genérico) a partir de seu nome de arquivo e baixam a variante de correspondência exata da pasta `downloads/`, evitando incompatibilidades acidentais de arquitetura durante as atualizações.
- **CLI fluxo de atualização do instalador de configuração**: CLI agora espelha o comportamento de GUI para instalações de configuração — ao executar a partir de `Program Files`, ele baixa o instalador de configuração `.exe` mais recente e o executa silenciosamente (`/VERYSILENT /NORESTART`) em vez de tentar uma troca binária no local.

---

## [1.0.3] - 2026-03-26

### ✨ Alterado

- Substituição do rótulo de compilação local padrão de `REL-LOCAL` para `BUILD-UNKNOWN` em ferramentas de tempo de execução/versão e manifestos gerados.
- GUI agora inclui uma ação de menu superior **Changelog** e um menu suspenso **Versão** com entrada explícita de verificação de versão.
- Adicionada verificação automática de versão de inicialização em GUI com ações pop-up de atualização (**Atualizar** / **Mais tarde**), além de manipulação de fluxo de atualização para configuração congelada/distribuições portáteis.
- Geração de código de construção atualizada para `REL-U<unix_ms>` estilo unix em versões alteradas (`patch/minor/major`).

## [1.0.2] - 2026-03-23

### ✨ Adicionado

- **Console de depuração (GUI)**
Um botão `⚙ Debug` dedicado no canto superior direito do cabeçalho GUI abre um console de terminal com tema escuro que registra todos os eventos do aplicativo em tempo real. Os eventos capturados incluem: inicialização do aplicativo, alterações de idioma, todos os cliques de botão (login aberto, token do Exchange, token de atualização, token de acesso/atualização de cópia, tutorial), estados de solicitação HTTP (envio/sucesso/falha), etapas de fluxo PKCE, operações da área de transferência, gravações de configuração e avisos. Todas as mensagens de depuração estão totalmente localizadas em todos os 11 idiomas suportados. O console suporta transmissão ao vivo de novas mensagens enquanto abertas, pré-preenchimento de logs históricos desde o início da sessão, um botão **Copiar tudo** e um botão **Limpar**.

## [1.0.1] - 2026-03-22

### ✨ Adicionado

- **Limpador README inteligente para lançamentos**
Remove automaticamente seções de idioma de localização do arquivo `` ao compilar o `.zip` distribuível, substituindo links internos por links GitHub absolutos.
- **Suporte ao instalador duplo unificado**
O script construtor InnoSetup agora gera um instalador unificado que solicita aos usuários finais que instalem opcionalmente o CLI independente ou o GUI gráfico.

### 🐞 Corrigido

- **Resolução do caminho de construção do instalador**
Corrigido um problema de incompatibilidade de caminho crítico em `make_installer_iss_dual.py`, onde `iscc` não conseguiu localizar `app\pixiv_oauth.ico` gerando arquivos de construção diretamente no diretório `scripts\` configurado.

## [1.0.0] - 2026-03-21

### ✨ Adicionado

- Distribuições executáveis ​​independentes iniciais (`.exe`) compiladas para os modos GUI e CLI.
- Integração inicial otimizada sem servidor sincronizada com Vercel com detecção automática de idioma.
- Passagem de ofuscação extrema de JavaScript adicionada para endpoints da web.
