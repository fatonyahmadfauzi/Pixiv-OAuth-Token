(function addStructuredData() {
  const DOMAIN = 'https://pixiv-o-auth-token.vercel.app';

  const schema = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebSite',
        '@id': DOMAIN + '/#website',
        'url': DOMAIN + '/',
        'name': 'Pixiv OAuth Web',
        'description': 'Generate and refresh Pixiv OAuth tokens using CLI, GUI, or Web with secure PKCE flow.',
        'author': {
          '@type': 'Person',
          'name': 'Fatony Ahmad Fauzi',
          'url': 'https://github.com/fatonyahmadfauzi'
        },
        'inLanguage': 'en-US'
      },
      {
        '@type': 'SoftwareApplication',
        'name': 'Pixiv OAuth Token Helper',
        'applicationCategory': 'DeveloperApplication',
        'operatingSystem': 'Windows, Web',
        'url': DOMAIN + '/',
        'downloadUrl': DOMAIN + '/downloads',
        'offers': { '@type': 'Offer', 'price': '0', 'priceCurrency': 'USD' },
        'author': {
          '@type': 'Person',
          'name': 'Fatony Ahmad Fauzi',
          'url': 'https://github.com/fatonyahmadfauzi'
        },
        'sameAs': ['https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token'],
        'description': 'Generate and refresh Pixiv OAuth tokens using CLI, GUI, or Web (PKCE). Supports deployment on Vercel.'
      },
      {
        '@type': 'SiteLinksSearchBox',
        'url': DOMAIN + '/',
        'potentialAction': {
          '@type': 'SearchAction',
          'target': {
            '@type': 'EntryPoint',
            'urlTemplate': DOMAIN + '/documentation'
          },
          'query-input': 'required name=search_term_string'
        }
      },
      {
        '@type': 'SiteNavigationElement',
        'name': ['Downloads', 'Download for Windows', 'Download for Python'],
        'url': [
          DOMAIN + '/downloads',
          DOMAIN + '/downloads#windowsPanel',
          DOMAIN + '/downloads#pythonPanel'
        ]
      }
    ]
  };

  const script = document.createElement('script');
  script.type = 'application/ld+json';
  script.text = JSON.stringify(schema, null, 2);
  document.head.appendChild(script);
})();
