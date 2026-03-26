# Registro de alterações

All notable changes to the "Pixiv OAuth Token" toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


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
Remove automaticamente seções de idioma de localização do arquivo `` ao compilar o `.zip` distribuível, substituindo links internos por links GitHub absolutos.
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
