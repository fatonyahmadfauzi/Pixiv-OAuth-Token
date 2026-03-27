(function () {
  const i18n = {
    en: { title: "Changelog", desc: "Auto-fetched from <code>CHANGELOG.md</code> on the <a href=\"https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token\" target=\"_blank\" rel=\"noopener\">GitHub repository</a>.", home: "Homepage", docs: "Documentation", dl: "Download", tut: "Tutorial" },
    id: { title: "Changelog", desc: "Diambil otomatis dari <code>CHANGELOG.md</code> pada <a href=\"https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token\" target=\"_blank\" rel=\"noopener\">repository GitHub</a>.", home: "Beranda", docs: "Dokumentasi", dl: "Unduh", tut: "Tutorial" },
    jp: { title: "変更履歴", desc: "<a href=\"https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token\" target=\"_blank\" rel=\"noopener\">GitHubリポジトリ</a>の <code>CHANGELOG.md</code> から自動取得。", home: "ホーム", docs: "ドキュメント", dl: "ダウンロード", tut: "チュートリアル" },
    zh: { title: "更新日志", desc: "自动从 <a href=\"https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token\" target=\"_blank\" rel=\"noopener\">GitHub 仓库</a> 的 <code>CHANGELOG.md</code> 获取。", home: "主页", docs: "文档", dl: "下载", tut: "教程" }
  };
  function apply() {
    const lang = (document.documentElement.lang || "en").toLowerCase();
    const t = i18n[lang] || i18n[lang.split("-")[0]] || i18n.en;
    const title = document.getElementById("changelogPageTitle");
    const desc = document.getElementById("changelogPageDesc");
    const home = document.getElementById("navHomepageLabel");
    const docs = document.getElementById("navDocs");
    const dl = document.getElementById("navDownloads");
    const tut = document.getElementById("navTutorial");
    if (title) title.textContent = t.title;
    if (desc) desc.innerHTML = t.desc;
    if (home) home.textContent = t.home;
    if (docs) docs.textContent = t.docs;
    if (dl) dl.textContent = t.dl;
    if (tut) tut.textContent = t.tut;
  }
  apply();
  new MutationObserver(apply).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
})();
