(function addStructuredData() {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: 'Pixiv OAuth Token Helper',
    applicationCategory: 'DeveloperApplication',
    operatingSystem: 'Windows, Web',
    url: 'https://pixiv-oauth-token.vercel.app/',
    downloadUrl: 'https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest',
    author: {
      '@type': 'Person',
      name: 'Fatony Ahmad Fauzi'
    },
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'USD'
    },
    sameAs: [
      'https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token'
    ],
    description:
      'Generate and refresh Pixiv OAuth tokens using CLI, GUI, or Web (PKCE). Supports deployment on Netlify and Vercel.'
  };

  const script = document.createElement('script');
  script.type = 'application/ld+json';
  script.text = JSON.stringify(schema);
  document.head.appendChild(script);
})();
