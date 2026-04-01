export function injectSchema() {
  const BASE_URL = "https://pixiv-o-auth-token.vercel.app";
  const schema = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebSite",
        "@id": BASE_URL + "/#website",
        url: BASE_URL + "/",
        name: "Pixiv OAuth Token Helper",
        description:
          "Generate and refresh Pixiv OAuth tokens using CLI, GUI, or Web with secure PKCE flow.",
        author: {
          "@type": "Person",
          name: "Fatony Ahmad Fauzi",
          url: "https://github.com/fatonyahmadfauzi",
        },
        inLanguage: "en-US",
      },
      {
        "@type": "SoftwareApplication",
        name: "Pixiv OAuth Token Helper",
        applicationCategory: "DeveloperApplication",
        operatingSystem: "Windows, Web",
        url: BASE_URL + "/",
        downloadUrl: BASE_URL + "/downloads",
        offers: { "@type": "Offer", price: "0", priceCurrency: "USD" },
        author: {
          "@type": "Person",
          name: "Fatony Ahmad Fauzi",
          url: "https://github.com/fatonyahmadfauzi",
        },
        sameAs: ["https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token"],
        description:
          "Pixiv OAuth Token Helper. Supports Windows, GUI, or Web (PKCE). Generate and refresh Pixiv tokens with secure PKCE deployment on Vercel or Python.",
      },
      {
        "@type": "WebSite",
        url: BASE_URL + "/",
        potentialAction: {
          "@type": "SearchAction",
          target: {
            "@type": "EntryPoint",
            urlTemplate: BASE_URL + "/?_term_string={search_term_string}",
          },
          "query-input": "required name=search_term_string",
        },
      },
      {
        "@type": "SiteLinksSearchBox",
        name: ["Downloads", "Documentation", "Download for Windows"],
        url: [
          BASE_URL + "/downloads",
          BASE_URL + "/documentation",
          BASE_URL + "#windowsPanel",
        ],
      },
    ],
  };

  const script = document.createElement("script");
  script.type = "application/ld+json";
  script.textContent = JSON.stringify(schema, null, 2);
  document.head.appendChild(script);
}
