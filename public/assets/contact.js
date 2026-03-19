// contact.js
// Handles success redirect messages without violating CSP rules

if (window.location.search.includes('success=true')) {
  var cf = document.getElementById('contactForm');
  var cs = document.getElementById('contactSuccess');
  
  if (cf && cs) {
    cf.style.display = 'none';
    cs.style.display = 'flex';
  }
  
  // Clean URL silently
  window.history.replaceState({}, document.title, window.location.pathname);
}
