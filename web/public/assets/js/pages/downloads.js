import { q } from "../core/dom.js";
import { DOWNLOADS_BASE, RELEASE_BASE } from "../core/config.js";
import { copyToClipboard } from "../core/utils.js";
import { DISPLAY_LANG } from "../core/i18n.js";

/**
 * Returns --lang <code> suffix if page language is not English.
 * This ensures commands displayed on /jp/downloads automatically
 * include --lang jp, etc.
 */
function getLangSuffix() {
  // DISPLAY_LANG is resolved from URL prefix > localStorage > browser language
  return DISPLAY_LANG && DISPLAY_LANG !== "en" ? ` --lang ${DISPLAY_LANG}` : "";
}

function repoDownloadLink(name) {
  return `${DOWNLOADS_BASE}/${encodeURIComponent(name)}`;
}

export function setDownloadLinks(assets = {}) {
  const cliSetup = q("dlCliSetup"),
    cliPortable = q("dlCliPortable"),
    guiSetup = q("dlGuiSetup"),
    guiPortable = q("dlGuiPortable");
  if (cliSetup)
    cliSetup.href =
      assets.cliSetup || repoDownloadLink("Pixiv OAuth CLi Setup_latest.exe");
  if (cliPortable)
    cliPortable.href =
      assets.cliPortable ||
      repoDownloadLink("Pixiv OAuth CLi (Portable)_latest.exe");
  if (guiSetup)
    guiSetup.href =
      assets.guiSetup || repoDownloadLink("Pixiv OAuth GUi Setup_latest.exe");
  if (guiPortable)
    guiPortable.href =
      assets.guiPortable ||
      repoDownloadLink("Pixiv OAuth GUi (Portable)_latest.exe");
}

export function setupDownloadTabs() {
  const tabs = Array.from(
    document.querySelectorAll(".download-inline-tabs a[data-tab-target]"),
  );
  if (!tabs.length) return;
  const panels = Array.from(document.querySelectorAll(".download-tab-panel"));
  const activate = (targetId) => {
    tabs.forEach((tab) => {
      const isActive = tab.dataset.tabTarget === targetId;
      tab.classList.toggle("active", isActive);
      tab.setAttribute("aria-current", isActive ? "page" : "false");
    });
    panels.forEach((panel) => {
      panel.classList.toggle("active", panel.id === targetId);
    });
  };
  tabs.forEach((tab) => {
    tab.addEventListener("click", (e) => {
      e.preventDefault();
      activate(tab.dataset.tabTarget);
    });
    tab.addEventListener("keydown", (e) => {
      const currentIndex = tabs.indexOf(tab);
      if (
        !(currentIndex < 0 || (e.key !== "ArrowRight" && e.key !== "ArrowLeft"))
      ) {
        e.preventDefault();
        const next =
          (currentIndex + (e.key === "ArrowRight" ? 1 : -1) + tabs.length) %
          tabs.length;
        activate(tabs[next].dataset.tabTarget);
        tabs[next].focus();
      }
    });
  });
  activate("downloadTabPanel");
}

export function setupArchDownloadRows() {
  const ARCH_MAP = { x86: "x86", x64: "x64", arm64: "ARM64" };
  [
    {
      selectId: "archSelectGuiSetup",
      btnId: "btnGuiSetupArch",
      prefix: "Pixiv OAuth GUi Setup",
    },
    {
      selectId: "archSelectCliSetup",
      btnId: "btnCliSetupArch",
      prefix: "Pixiv OAuth CLi Setup",
    },
    {
      selectId: "archSelectGuiPortable",
      btnId: "btnGuiPortableArch",
      prefix: "Pixiv OAuth GUi (Portable)",
    },
    {
      selectId: "archSelectCliPortable",
      btnId: "btnCliPortableArch",
      prefix: "Pixiv OAuth CLi (Portable)",
    },
  ].forEach(({ selectId, btnId, prefix }) => {
    const select = q(selectId),
      btn = q(btnId);
    if (!select || !btn) return;
    const apply = () => {
      const arch = select.value || "x64";
      btn.href = repoDownloadLink(`${prefix} ${ARCH_MAP[arch]}_latest.exe`);
    };
    select.addEventListener("change", apply);
    apply();
  });
}

function setCommandBlocks(assets = {}) {
  const files = {
    guiPortable: {
      x64:
        assets.guiPortableX64 ||
        repoDownloadLink("Pixiv OAuth GUi (Portable) x64_latest.exe"),
      x86:
        assets.guiPortableX86 ||
        repoDownloadLink("Pixiv OAuth GUi (Portable) x86_latest.exe"),
      arm64:
        assets.guiPortableArm64 ||
        repoDownloadLink("Pixiv OAuth GUi (Portable) ARM64_latest.exe"),
    },
    cliPortable: {
      x64:
        assets.cliPortableX64 ||
        repoDownloadLink("Pixiv OAuth CLi (Portable) x64_latest.exe"),
      x86:
        assets.cliPortableX86 ||
        repoDownloadLink("Pixiv OAuth CLi (Portable) x86_latest.exe"),
      arm64:
        assets.cliPortableArm64 ||
        repoDownloadLink("Pixiv OAuth CLi (Portable) ARM64_latest.exe"),
    },
    guiSetup: {
      x64:
        assets.guiSetupX64 ||
        repoDownloadLink("Pixiv OAuth GUi Setup x64_latest.exe"),
      x86:
        assets.guiSetupX86 ||
        repoDownloadLink("Pixiv OAuth GUi Setup x86_latest.exe"),
      arm64:
        assets.guiSetupArm64 ||
        repoDownloadLink("Pixiv OAuth GUi Setup ARM64_latest.exe"),
    },
    cliSetup: {
      x64:
        assets.cliSetupX64 ||
        repoDownloadLink("Pixiv OAuth CLi Setup x64_latest.exe"),
      x86:
        assets.cliSetupX86 ||
        repoDownloadLink("Pixiv OAuth CLi Setup x86_latest.exe"),
      arm64:
        assets.cliSetupArm64 ||
        repoDownloadLink("Pixiv OAuth CLi Setup ARM64_latest.exe"),
    },
  };
  const archOrder = [
    ["x64", "64-Bit"],
    ["x86", "32-Bit"],
    ["arm64", "ARM 64-Bit"],
  ];
  const psCommands = [],
    cmdCommands = [];
  [
    ["guiPortable", "Portable GUI"],
    ["cliPortable", "Portable CLI"],
    ["guiSetup", "Setup GUI"],
    ["cliSetup", "Setup CLI"],
  ].forEach(([key, name]) => {
    archOrder.forEach(([arch, archLabel]) => {
      const url = files[key][arch];
      psCommands.push({
        title: `${name} ${archLabel}`,
        value: `Invoke-WebRequest "${url}" -OutFile "Pixiv OAuth ${name} (${archLabel}).exe"`,
      });
      cmdCommands.push({
        title: `${name} ${archLabel}`,
        value: `curl -L "${url}" -o "Pixiv OAuth ${name} (${archLabel}).exe"`,
      });
    });
  });

  const renderList = (containerId, commands) => {
    const root = q(containerId);
    if (!root) return;
    root.innerHTML = "";
    commands.forEach((item) => {
      const box = document.createElement("div");
      box.className = "cmd-command-item";
      const title = document.createElement("small");
      title.className = "cmd-command-label";
      title.textContent = item.title;
      const row = document.createElement("div");
      row.className = "cmd-command-row";
      const code = document.createElement("code");
      code.className = "cmd-command-code";
      code.textContent = item.value;
      const copyBtn = document.createElement("button");
      copyBtn.className = "cmd-copy-btn";
      copyBtn.type = "button";
      copyBtn.setAttribute("aria-label", `Copy ${item.title}`);
      copyBtn.innerHTML = '<i class="bi bi-copy" aria-hidden="true"></i>';
      copyBtn.addEventListener("click", async () => {
        await navigator.clipboard.writeText(item.value);
        const output = q("output");
        if (output) output.textContent = `Command copied: ${item.title}`;
      });
      row.appendChild(code);
      row.appendChild(copyBtn);
      box.appendChild(title);
      box.appendChild(row);
      root.appendChild(box);
    });
  };
  renderList("psCmdList", psCommands);
  renderList("cmdCmdList", cmdCommands);
  const ps = q("psCmd"),
    cmd = q("cmdCmd");
  if (ps) ps.textContent = psCommands.map((x) => x.value).join("n");
  if (cmd) cmd.textContent = cmdCommands.map((x) => x.value).join("n");
}

export function setupDownloadCategorySwitch() {
  const items = Array.from(document.querySelectorAll("[data-download-panel]")),
    panels = Array.from(document.querySelectorAll(".download-category-panel"));
  if (!items.length || !panels.length) return;
  const activatePanel = (panelId) => {
    items.forEach((item) => {
      const active = item.dataset.downloadPanel === panelId;
      item.classList.toggle("active", active);
      item.setAttribute("aria-pressed", active ? "true" : "false");
    });
    panels.forEach((panel) => {
      const active = panel.id === panelId;
      panel.classList.toggle("active", active);
      panel.hidden = !active;
    });
  };
  items.forEach((item) => {
    item.addEventListener("click", () =>
      activatePanel(item.dataset.downloadPanel),
    );
    item.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        activatePanel(item.dataset.downloadPanel);
      }
    });
  });
}

export function setupCommandCopyButtons() {
  document.querySelectorAll("[data-copy-text]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const text = btn.getAttribute("data-copy-text") || "";
      if (text) {
        await navigator.clipboard.writeText(text);
        const output = q("output");
        if (output) output.textContent = "Command copied.";
      }
    });
  });
}

export function setupMobilePlatformDropdown() {
  const select = document.getElementById("mobilePlatformSelect");
  if (select) {
    select.addEventListener("change", () => {
      const targetId = select.value,
        panels = document.querySelectorAll(".download-category-panel"),
        sidebarItems = document.querySelectorAll(
          ".download-showcase-sidebar li",
        );
      panels.forEach((p) => {
        p.hidden = p.id !== targetId;
        p.classList.toggle("active", p.id === targetId);
      });
      sidebarItems.forEach((li) => {
        li.classList.toggle("active", li.dataset.downloadPanel === targetId);
        li.setAttribute(
          "aria-pressed",
          li.dataset.downloadPanel === targetId ? "true" : "false",
        );
      });
    });
  }
}

export async function hydrateReleaseAssets() {
  setDownloadLinks();
  setCommandBlocks();
  updatePySdkInstallCommands();
}

/**
 * Updates the Python SDK install commands on the page
 * to include --lang <code> based on current page locale.
 *
 * Q1: When user visits /jp/downloads, commands get --lang jp appended.
 * Q2: If --lang not provided by user, install scripts fallback to OS language.
 */
export function updatePySdkInstallCommands() {
  const langSuffix = getLangSuffix();

  const PS_BASE = "irm https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/install.ps1 | iex";
  const CMD_BASE = `powershell -Command "irm https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/install.ps1 | iex"`;
  const BASH_BASE = "bash <(curl -sL https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/install.sh)";

  // How to pass lang to PowerShell installer (env var approach, works with pipe)
  const psCmd  = langSuffix ? `$env:PIXIV_LANG='${DISPLAY_LANG}'; ${PS_BASE}` : PS_BASE;
  const cmdCmd = langSuffix ? `powershell -Command "$env:PIXIV_LANG='${DISPLAY_LANG}'; irm https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/install.ps1 | iex"` : CMD_BASE;
  const bashCmd = langSuffix ? `${BASH_BASE}${langSuffix}` : BASH_BASE;

  // Update <code> elements
  const winCode   = q("dlPyDirectWinCode");
  const cmdCode   = q("dlPyDirectCmdCode");
  const linuxCode = q("dlPyDirectLinuxCode");

  if (winCode)   winCode.textContent   = psCmd;
  if (cmdCode)   cmdCode.textContent   = cmdCmd;
  if (linuxCode) linuxCode.textContent = bashCmd;

  // Update copy buttons' data-copy-text
  document.querySelectorAll(".cmd-copy-btn[aria-label='Copy PowerShell command']").forEach(btn => {
    btn.setAttribute("data-copy-text", psCmd);
  });
  document.querySelectorAll(".cmd-copy-btn[aria-label='Copy CMD command']").forEach(btn => {
    btn.setAttribute("data-copy-text", cmdCmd);
  });
  document.querySelectorAll(".cmd-copy-btn[aria-label='Copy bash command']").forEach(btn => {
    btn.setAttribute("data-copy-text", bashCmd);
  });
}
